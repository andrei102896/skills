"""Grep facts about changed declarations: unused exports, one-caller helpers, one-importer defaults."""
import os
import re

from gitutil import CODE_EXT, TEST_PATH_RE, git, sh

USE_EXT = CODE_EXT + (".json", ".yml", ".yaml", ".php")
TINY_FILE_LINES = 5
DECL = re.compile(r"^\+\s*(export\s+)?(?:default\s+)?(?:async\s+)?(const|let|function|class|type|interface|enum)\s+(\w+)(.*)")
DEFAULT_EXPORT_FN_RE = re.compile(r"^\+\s*export default (async )?(\(|function|\w+ =>)")
EXPORT_DEFAULT = re.compile(r"^\+\s*export\s+default\b")
IS_FN = re.compile(r"\s*(:[^=]+)?=\s*(async\s*)?(\(|\w+\s*=>|function)")
DECLARED_NAME_RE = re.compile(r"(?:function\*?|const|let|class|interface|type|enum)\s+(\w+)")
REMOVED_EXPORT = re.compile(
    r"^-\s*export\s+(?:default\s+)?(?:async\s+)?(?:const|let|function\*?|class|type|interface|enum)\s+(\w+)")


def stem_of(path):
    return os.path.splitext(os.path.basename(path))[0]


def head_text(head, path):
    return git("show", f"{head}:{path}") or ""


def files_mentioning(pattern, head, path, fixed=True, exts=CODE_EXT, tests=False):
    """Files at `head` (other than `path`) matching a word, or an extended regex when not fixed."""
    flag = "-lw" if fixed else "-lE"
    code, out, _ = sh("git", "grep", flag, "-e", pattern, head, "--", *[f"*{e}" for e in exts])
    found = set()
    for line in out.splitlines() if code == 0 else []:
        hit = line.split(":", 1)[1]
        if hit != path and (tests or not TEST_PATH_RE.search(hit)):
            found.add(hit)
    return sorted(found)


def exported_later(name, text):
    n = re.escape(name)
    pattern = rf"^\s*export\s*\{{[^}}]*\b{n}\b|module\.exports\s*=\s*(?:\{{[^}}]*\b{n}\b|{n}\b)|\bexports\.{n}\s*="
    return re.search(pattern, text, re.M) is not None


def fact_checks(path, head, diff):
    """Notes for the `> **facts:**` lines of one diff (a hunk or a whole file)."""
    if TEST_PATH_RE.search(path) or not path.endswith(CODE_EXT):
        return []
    text = head_text(head, path)
    notes = []
    for line in diff.splitlines():
        m = DECL.match(line)
        if m:
            if EXPORT_DEFAULT.match(line):
                continue  # default exports are found through their file path
            name = m.group(3)
            exported = bool(m.group(1)) or exported_later(name, text)
            is_fn = m.group(2) == "function" or IS_FN.match(m.group(4)) is not None
            same = len(re.findall(rf"\b{re.escape(name)}\b", text)) - 1
            if exported and not files_mentioning(name, head, path, exts=USE_EXT, tests=True):
                notes.append(f"[unused-export] `{name}` is exported; `git grep -w` finds it in no other file "
                             "(code, json, yaml, php; tests included)")
            elif not exported and is_fn and same == 1:
                notes.append(f"[one-caller] `{name}` is not exported and its name occurs once more in this file "
                             "(word grep)")
        elif DEFAULT_EXPORT_FN_RE.match(line) and sum(1 for t in text.splitlines() if t.strip()) <= TINY_FILE_LINES:
            stem = re.sub(r"([.^$*+?()\[\]{}|\\])", r"\\\1", stem_of(path))
            users = files_mentioning(f"['\"/]{stem}['\"]", head, path, fixed=False)
            if len(users) == 1:
                notes.append(f"[one-importer] the default export: `git grep` finds one file naming `{stem_of(path)}` "
                             f"in an import path, `{users[0]}`")
    return notes


def changed_exports(path, head, hunks):
    """(exported names touched by the hunks + the file stem, exports the hunks removed)."""
    text = head_text(head, path)
    candidates = set()
    for h in hunks:
        candidates.update(m.group(3) for m in map(DECL.match, h["lines"]) if m)
        above = []
        for line in h["lines"]:
            if line.startswith(("+", "-")):
                break
            above += DECLARED_NAME_RE.findall(line)
        candidates.update(above or DECLARED_NAME_RE.findall(h["symbol"]))
    exported = sorted(
        n for n in candidates
        if re.search(rf"^export\s+(default\s+)?((async\s+)?function\*?|const|let|class|type|interface|enum)\s+{n}\b"
                     rf"|^export\s*\{{[^}}]*\b{n}\b", text, re.M))
    removed = {m.group(1) for h in hunks for m in map(REMOVED_EXPORT.match, h["lines"]) if m}
    stem = stem_of(path)
    return exported + ([stem] if stem != "index" and stem not in exported else []), sorted(removed - set(exported))
