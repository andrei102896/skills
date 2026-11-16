"""Turn a diff into a call-ordered markdown index of hunks, routed rules, grep facts and outside callers.

Usage: walkthrough.py --base <sha> --head <sha> [--zone <prefix>]... [--zones] [-o <path>]
--zones prints the zone list and writes nothing. Default output:
~/.cache/reviewer/<repo>/walkthrough/<branch>[--<zone>+<zone>].md
"""
import argparse
import glob
import os
import re
import sys
from collections import Counter

from callers import MODULE_SPEC_RE, outside_callers, resolve
from facts import changed_exports, fact_checks
from gitutil import CODE_EXT, STYLE_EXT, TEST_PATH_RE, branch_key, current_branch, git, read, repo_name, sh, snapshot_tree
from routing import categorize, groups

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUNK_RE = re.compile(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@ ?(.*)")


def span(text):
    """(end line, added, removed) of one hunk text starting with its @@ header."""
    lines = text.splitlines()
    m = HUNK_RE.match(lines[0])
    end = int(m.group(1)) + max(int(m.group(2) or 1), 1) - 1
    body = lines[1:]
    return end, sum(1 for l in body if l.startswith("+")), sum(1 for l in body if l.startswith("-"))


def parse_hunks(base, head, path):
    hunks = []
    for line in (git("diff", "-U3", f"{base}..{head}", "--", path) or "").splitlines():
        m = HUNK_RE.match(line)
        if m:
            hunks.append({"header": line, "start": int(m.group(1)), "symbol": m.group(3).strip(), "lines": []})
        elif hunks and (line == "" or line[0] in "+- "):
            hunks[-1]["lines"].append(line)
    for h in hunks:
        h["text"] = "\n".join([h["header"]] + h["lines"])
    return hunks


def zones(files, max_size=25, min_size=4):
    out = []

    def split(group, depth):
        if len(group) <= max_size:
            common = os.path.commonpath(group)
            out.append((os.path.dirname(common) if common in group else common, group))
            return
        buckets = {}
        for f in group:
            parts = f.split("/")
            buckets.setdefault("/".join(parts[:min(depth, len(parts) - 1)]), []).append(f)
        if len(buckets) == 1:
            if depth < 12:
                return split(group, depth + 1)
            out.append((next(iter(buckets)), group))
            return
        for key in sorted(buckets):
            if len(buckets[key]) > max_size:
                split(buckets[key], depth + 1)
            else:
                out.append((key, buckets[key]))

    split(sorted(files), 1)
    out.sort(key=lambda z: -len(z[1]))
    small = sorted(f for _, g in out if len(g) < min_size for f in g)
    return [z for z in out if len(z[1]) >= min_size] + ([("scattered", small)] if small else [])


def print_zones(title, files):
    print(f"{title} — {len(files)} files\n")
    for prefix, group in zones(files):
        print(f"{len(group):4}  {prefix or '.'}/" if prefix != "scattered" else f"{len(group):4}  scattered")
        cut = len(prefix) + 1 if prefix not in ("", "scattered") else 0
        for f in sorted(group)[:6]:
            print(f"        {f[cut:]}")
        if len(group) > 6:
            print(f"        … {len(group) - 6} more")


def pick_zones(files, picks):
    known = dict(zones(files))
    chosen = []
    for p in ("" if p in (".", "./") else p.rstrip("/") for p in picks):
        hits = known.get(p) or [f for f in files if f.startswith(p + "/")]
        if not hits:
            sys.exit(f"no files in zone {p} — run --zones for the list")
        chosen += [f for f in hits if f not in chosen]
    return chosen


def order(files):
    """(files in call order, caller before callee; in-diff import edges)."""
    known = set(files)
    edges = {f: [] for f in files}
    for f in files:
        if os.path.isfile(f) and f.endswith(CODE_EXT + STYLE_EXT):
            for spec in MODULE_SPEC_RE.findall(read(f)):
                target = resolve(spec, f, known)
                if target in known and target != f and target not in edges[f]:
                    edges[f].append(target)
    indeg = Counter(d for f in files for d in edges[f])

    def reach(f, seen):
        for d in edges[f]:
            if d not in seen:
                seen.add(d)
                reach(d, seen)
        return seen

    roots = sorted((f for f in files if not indeg[f]), key=lambda f: -len(reach(f, set())))
    out, seen = [], set()

    def visit(f):
        if f not in seen:
            seen.add(f)
            out.append(f)
            for d in sorted(edges[f]):
                visit(d)

    for f in roots + files:
        visit(f)
    return out, edges


def guard(head, files, name):
    if git("rev-parse", "HEAD") == head and sh("git", "diff", "--quiet", "HEAD", "--", *files)[0] == 0:
        return
    if git("rev-parse", f"{head}^") == git("rev-parse", "HEAD") and snapshot_tree() == git("rev-parse", f"{head}^{{tree}}"):
        return
    sys.exit(f"checkout is not {name} @ {head[:8]}, or has local edits in its files — check out {name} and pull "
             f"(or `git worktree add <dir> {head[:8]}`), then rerun")


def rule_names():
    names = set()
    for d in (os.path.join(".claude", "review-rules"), os.path.join(SKILL_DIR, "rules")):
        names.update(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(d, "*.md")))
    names.discard("_do-not-flag")
    return names


def render_file(i, path, base, head, changed, edges, hunk_no, group_hunks, rows):
    lines = [f"## {i}. `{path}`", ""]
    hunks = parse_hunks(base, head, path)
    if edges[path]:
        lines += ["Calls into, later in this review: " + ", ".join(f"`{os.path.basename(d)}`" for d in edges[path]), ""]
    if path.endswith(CODE_EXT + STYLE_EXT):
        names, removed = changed_exports(path, head, hunks)
        still, _ = outside_callers(path, changed, removed, head)
        callers, generic = outside_callers(path, changed, names, head)
        searched = [n for n in names if n not in generic]
        if still:
            lines += [f"**Still import what this change removes** ({', '.join(f'`{n}`' for n in removed)}):"]
            lines += [f"- `{f}`" for f in still]
        if callers:
            lines += ["**Callers outside the diff — unchanged, and not proven by this change** "
                      f"(of {', '.join(f'`{n}`' for n in searched)}):"]
            lines += [f"- `{f}`" for f in callers]
        if generic:
            lines += ["Generic names, outside callers not searched (check with LSP): "
                      + ", ".join(f"`{n}`" for n in generic)]
        if still or callers or generic:
            lines.append("")
    for h in hunks:
        hunk_no += 1
        end, added, removed = span(h["text"])
        where = f" — in `{h['symbol']}`" if h["symbol"] else ""
        lines.append(f"### H{hunk_no}. `{path}:{h['start']}-{end}`{where} · +{added} −{removed}")
        labels, rules = categorize(path, h["text"])
        if rules:
            lines.append(f"> **check:** {', '.join(rules)} — as {', '.join(labels)}")
        lines += [f"> **facts:** {note}" for note in fact_checks(path, head, h["text"])]
        for name, group_rules, _ in rows:
            if set(rules) & set(group_rules):
                group_hunks[name].append(f"H{hunk_no}")
        lines.append("")
    return lines, hunk_no


def build(base, head, title, files, rows):
    ordered, edges = order(files)
    tests = [f for f in ordered if TEST_PATH_RE.search(f)]
    ordered = [f for f in ordered if not TEST_PATH_RE.search(f)]
    changed = set(files)
    hunk_no, body, group_hunks = 0, [], {name: [] for name, _, _ in rows}
    for i, path in enumerate(ordered, 1):
        lines, hunk_no = render_file(i, path, base, head, changed, edges, hunk_no, group_hunks, rows)
        body += lines
    b8, h8 = base[:8], head[:8]
    doc = [f"# Walkthrough — {title}", "",
           f"`{b8}..{h8}` · {len(files)} files, call order (caller before callee).",
           "This is an index of locations, not code: read a hunk with "
           f"`git diff -U8 {b8}..{h8} -- <file>`, its context with `sed -n '<a>,<b>p' <file>`.",
           "`check:` lines route rules to a hunk; `facts:` lines are grep leads to confirm, not findings.",
           "Each file lists the callers outside the diff that import what it changed.", "",
           "## Groups", "", "| group | rules | hunks |", "|---|---|---|"]
    every = f"all (H1–H{hunk_no})" if hunk_no else "all (none)"
    for name, group_rules, routed in rows:
        hunks = (", ".join(group_hunks[name]) or "none — skip") if routed else every
        doc.append(f"| {name} | {', '.join(group_rules)} | {hunks} |")
    doc += ["", "---", ""] + body
    if tests:
        doc += ["---", "", "## Tests in this diff (not inlined)", ""]
        for row in (git("diff", "--numstat", f"{base}..{head}", "--", *tests) or "").splitlines():
            added, removed, path = row.split("\t", 2)
            doc.append(f"- `{path}` +{added} −{removed}")
    return "\n".join(doc).rstrip() + "\n", ordered


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--zone", action="append", default=[])
    ap.add_argument("--zones", action="store_true")
    ap.add_argument("-o", dest="out")
    args = ap.parse_args(argv)
    out = os.path.abspath(args.out) if args.out else None
    root = git("rev-parse", "--show-toplevel") or sys.exit("not inside a git repository")
    os.chdir(root)
    base = git("rev-parse", "--verify", f"{args.base}^{{commit}}") or sys.exit(f"unknown base {args.base}")
    head = git("rev-parse", "--verify", f"{args.head}^{{commit}}") or sys.exit(f"unknown head {args.head}")
    files = (git("diff", "--name-only", f"{base}..{head}") or "").splitlines()
    branch = current_branch()
    name = branch_key(branch) if branch and branch != "HEAD" else f"detached-{head[:8]}"
    title = f"{base[:8]}..{head[:8]}"
    if args.zones:
        print_zones(title, files)
        return
    if args.zone:
        files = pick_zones(files, args.zone)
        picks = [p.rstrip("/") for p in args.zone]
        name += "--" + "+".join(p.replace("/", "-") for p in picks)
        title += " · zone " + ", ".join(picks)
    guard(head, files, name)
    doc, ordered = build(base, head, title, files, groups(rule_names()))
    out = out or os.path.expanduser(f"~/.cache/reviewer/{repo_name()}/walkthrough/{name}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"{out}  ({len(files)} files)")
    for i, path in enumerate(ordered, 1):
        print(f"{i:3}. {path}")


if __name__ == "__main__":
    main()
