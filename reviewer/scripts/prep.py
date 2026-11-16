"""All mechanical facts before a review, as one stdout block; decides stop or continue.

Usage: prep.py [<pr#|branch>] [--base <branch>] [--uncommitted] [--quick]
No argument reviews the checked-out branch (author mode, never needs `gh`); an argument reviews that GitHub PR.
Lines other steps parse: STOP:, UNCOMMITTED, RESUME, base:, range:, files:, ZONES REQUIRED, walkthrough:,
findings file:, prior findings:, pr:, pr comments:, stacked:.
"""
import datetime
import json
import os
import re
import shutil
import sys

from gitutil import branch_key, current_branch, git, repo_name, sh, snapshot

ZONE_THRESHOLD = 30
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
FINDING_ID_RE = re.compile(r"^- \*\*((?:\d+[a-z]?\.)?[A-D]\d+)\.")
TICKED_BOX_RE = re.compile(r"^\s*- \[x\] (request change|not now|not valid)")
AUTHOR = re.compile(r"^\s*- \[x\] .*\*\*author:\*\*")


def stop(reason):
    print(f"STOP: {reason}")
    sys.exit(1)


def parse_args(argv):
    target, base, uncommitted, quick = None, None, False, False
    args = list(argv)
    while args:
        a = args.pop(0)
        if a in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif a == "--base":
            base = args.pop(0) if args else stop("--base needs a branch")
        elif a == "--uncommitted":
            uncommitted = True
        elif a == "--quick":
            quick = True
        elif a.startswith("-"):
            stop(f"unknown option {a} — see prep.py --help")
        elif target:
            stop(f"one PR or branch at a time, got {target} and {a}")
        else:
            target = a
    return target, base, uncommitted, quick


def findings_dir():
    return os.path.expanduser(f"~/.claude/reviewer-findings/{repo_name()}")


def rounds(folder, key):
    """{round: path} for files named exactly `<key>-<YYYY-MM-DD>-r<n>.md` (a longer branch never counts)."""
    pattern = re.compile(re.escape(key) + r"-\d{4}-\d\d-\d\d-r(\d+)\.md")
    found = {}
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        m = pattern.fullmatch(name)
        if m:
            found[int(m.group(1))] = os.path.join(folder, name)
    return found


def next_round(folder, key):
    return max(rounds(folder, key), default=0) + 1


def read_findings(path):
    """[(id, tick, author-answered)] in file order; tick is the first ticked box or `undecided`."""
    found = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = FINDING_ID_RE.match(line)
            if m:
                found.append([m.group(1), "undecided", False])
            elif found:
                box = TICKED_BOX_RE.match(line)
                if box and found[-1][1] == "undecided":
                    found[-1][1] = box.group(1)
                if AUTHOR.match(line):
                    found[-1][2] = True
    return [tuple(f) for f in found]


def undecided(path):
    return [fid for fid, _, answered in read_findings(path) if not answered]


def related_findings(folder, key, base_key):
    parts = key.split("-")
    family = "-".join(parts[:2]) + "-" if len(parts) >= 2 else None
    own = re.compile(rf"({re.escape(key)}|{re.escape(base_key)})-\d{{4}}-\d\d-\d\d-r\d+\.md")
    names = sorted(os.listdir(folder)) if os.path.isdir(folder) else []
    return [os.path.join(folder, n) for n in names
            if n.endswith(".md") and (own.fullmatch(n) or (family and n.startswith(family)))]


def gh_json(*args):
    code, out, err = sh("gh", *args)
    return (json.loads(out) if out else None) if code == 0 else None


def guess_base(branch):
    if shutil.which("gh"):
        pr = gh_json("pr", "view", "--json", "baseRefName,state")
        if pr and pr.get("state") == "OPEN":
            return pr["baseRefName"], "pr target"
    remotes = [r[len("origin/"):] for r in (git("branch", "-r", "--format=%(refname:short)") or "").splitlines()
               if r.startswith("origin/")]
    parents = [b for b in remotes if b != "HEAD" and branch.startswith(b + "-")]
    if parents:
        return max(parents, key=len), "guessed"
    origin_head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if origin_head:
        return origin_head.split("/", 1)[1], "guessed"
    for b in ("main", "master"):
        if b in remotes or git("rev-parse", "--verify", "-q", b):
            return b, "guessed"
    stop("no base branch found — pass --base <branch>")


def resolve_base(base):
    if git("remote", "get-url", "origin"):
        sh("git", "fetch", "-q", "origin", base)
    if sh("git", "show-ref", "--verify", "-q", f"refs/remotes/origin/{base}")[0] == 0:
        return "origin/" + base
    if git("rev-parse", "--verify", "-q", base + "^{commit}"):
        return base
    stop(f"cannot resolve base {base} — pass --base <branch>")


def open_pr(arg):
    if not shutil.which("gh"):
        stop("PR mode needs the GitHub CLI `gh` (install it, then `gh auth login`); "
             "or check out the branch and run /reviewer with no argument")
    code, out, err = sh("gh", "pr", "view", arg, "--json", "number,title,url,baseRefName,headRefName,headRefOid")
    if code != 0:
        stop(f"no PR for {arg} — ask which PR ({err[:200]})")
    return json.loads(out)


def pr_comments(number):
    code, out, _ = sh("gh", "api", "--paginate", f"repos/{{owner}}/{{repo}}/pulls/{number}/comments")
    try:
        comments = json.loads(out) if code == 0 and out else []
    except ValueError:
        comments = []
    lines = []
    for c in comments:
        body = (c.get("body") or "").strip()
        gist = body.splitlines()[0][:100] if body else ""
        line = c.get("line") or c.get("original_line") or "?"
        lines.append(f"  {(c.get('user') or {}).get('login', '?')} {c.get('path')}:{line}: {gist}")
    return lines


def main(argv):
    target, base, uncommitted, quick = parse_args(argv)
    os.chdir(git("rev-parse", "--show-toplevel") or stop("not inside a git repository"))
    pr = open_pr(target) if target else None
    branch = pr["headRefName"] if pr else current_branch()
    if not branch or branch == "HEAD":
        stop("detached HEAD — check out the branch to review")
    key = branch_key(branch)
    folder = findings_dir()
    done = rounds(folder, key)
    if not quick and done and undecided(done[max(done)]):
        print(f"RESUME {done[max(done)]}: {', '.join(undecided(done[max(done)]))}")
        sys.exit(0)
    if pr:
        sh("git", "fetch", "-q", "origin", branch)
        now = git("rev-parse", "HEAD") or ""
        if now != pr["headRefOid"]:
            stop(f"HEAD {now[:8]} is not {branch} {pr['headRefOid'][:8]} — check out {branch} and pull, "
                 "or use --worktree")
    how = "given" if base else None
    if not base and pr:
        base, how = pr["baseRefName"], "pr target"
    elif not base:
        base, how = guess_base(branch)
    base_ref = resolve_base(base)
    head = git("rev-parse", "HEAD")
    mb = git("merge-base", base_ref, head) or stop(f"no common ancestor of {base_ref} and HEAD — pass --base")
    dirty = sorted(set((git("diff", "--name-only", "HEAD") or "").splitlines()
                       + (git("ls-files", "--others", "--exclude-standard") or "").splitlines()))
    if uncommitted or quick:
        head, dirty = snapshot() or stop("could not snapshot the working tree"), []
    files = (git("diff", "--name-only", mb, head) or "").splitlines()

    if pr:
        print(f"pr: #{pr['number']} {pr['title']} {pr['url']}")
    print(f"base: {base_ref} ({how})")
    print(f"range: {mb}..{head}")
    print(f"files: {len(files)}")
    if len(files) > ZONE_THRESHOLD:
        print("ZONES REQUIRED")
    print(f"walkthrough: python3 -B {os.path.join(SCRIPTS, 'walkthrough.py')} --base {mb} --head {head}")
    if not quick:
        n = next_round(folder, key)
        today = datetime.date.today().isoformat()
        print(f"findings file: {os.path.join(folder, f'{key}-{today}-r{n}.md')} (r{n})")
    prior = [(os.path.basename(p), f) for p in related_findings(folder, key, branch_key(base)) for f in read_findings(p)]
    print("prior findings:" + ("" if prior else " none"))
    for name, (fid, tick, _) in prior:
        print(f"  {name}: {fid} {tick}")
    if pr:
        comments = pr_comments(pr["number"])
        print("pr comments:" + ("" if comments else " none"))
        for line in comments:
            print(line)
    if shutil.which("gh"):
        for s in gh_json("pr", "list", "--base", branch, "--state", "open", "--json", "number,headRefName") or []:
            print(f"stacked: {s['headRefName']} (#{s['number']})")
    if dirty:
        print(f"UNCOMMITTED {len(dirty)}: {', '.join(dirty[:5])}")
    elif not files:
        stop(f"nothing committed on {branch} since {base_ref} — wrong base? pass --base")
    sys.exit(1 if dirty else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
