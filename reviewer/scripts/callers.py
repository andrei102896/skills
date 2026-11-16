"""Files outside the diff that import what a changed file exports: word `git grep` + import check."""
import glob
import json
import os
import re
from functools import lru_cache

from facts import files_mentioning, stem_of
from gitutil import CODE_EXT, STYLE_EXT, read

RESOLVE = [""] + list(CODE_EXT) + list(STYLE_EXT) + ["/index" + e for e in CODE_EXT]
MODULE_SPEC_RE = re.compile(r"""(?:from|import|require\()\s*\(?['"]([^'"]+)['"]""")
IMPORT_STATEMENT_RE = re.compile(r"""^import\s+(?:([^'";]+?)\s+from\s+)?['"]([^'"]+)['"]""", re.M)
REEXPORT_FROM_RE = re.compile(r"""^export\s[^;]*?from\s*['"]([^'"]+)['"]""", re.M)
# A word grep on these returns half the repo; the correctness agent checks them with LSP instead.
GENERIC = {"get", "set", "map", "t", "it", "dispatch", "init", "run", "main", "index", "default", "data", "value",
           "config", "update", "create", "remove", "render", "handler", "props", "state", "type", "types", "utils",
           "helpers", "constants", "styles", "App"}


def strip_jsonc(text):
    """JSON with comments and trailing commas (tsconfig style) to plain JSON, keeping strings intact."""
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\":
                out.append(text[i + 1:i + 2])
                i += 1
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
            out.append(c)
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        else:
            out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


@lru_cache(maxsize=None)
def aliases():
    """([(pattern, target)], [baseUrl dirs]) from the repo-root tsconfig*/jsconfig* files."""
    pairs, base_dirs = [], []
    for cfg in sorted(glob.glob("tsconfig*.json") + glob.glob("jsconfig*.json")):
        try:
            opts = json.loads(strip_jsonc(read(cfg))).get("compilerOptions") or {}
        except (ValueError, AttributeError):
            continue
        base = os.path.normpath(opts.get("baseUrl", "."))
        if "baseUrl" in opts:
            base_dirs.append(base)
        for key, targets in (opts.get("paths") or {}).items():
            pairs += [(key, os.path.normpath(os.path.join(base, t))) for t in targets]
    return pairs, base_dirs


def resolve(spec, importer, known):
    """Repo-relative file an import specifier points to, or None for a package."""
    if spec.startswith("."):
        bases = [os.path.normpath(os.path.join(os.path.dirname(importer), spec))]
    else:
        pairs, base_dirs = aliases()
        bases = []
        for key, target in pairs:
            if key.endswith("*") and spec.startswith(key[:-1]):
                bases.append(target.replace("*", spec[len(key) - 1:]))
            elif spec == key:
                bases.append(target)
        bases += [os.path.normpath(os.path.join(b, spec)) for b in base_dirs]
    for b in bases:
        for e in RESOLVE:
            if b + e in known or os.path.isfile(b + e):
                return b + e
    return None


def reexports(target, path, known, hops=2):
    """True when `target` is `path` or re-exports it through at most `hops` barrel files."""
    if target == path:
        return True
    if not target or hops == 0 or not os.path.isfile(target):
        return False
    return any(reexports(resolve(s, target, known), path, known, hops - 1) for s in REEXPORT_FROM_RE.findall(read(target)))


def outside_callers(path, changed, names, head):
    """(files outside `changed` importing one of `names` from `path`, generic names not searched)."""
    stem = stem_of(path)
    found, skipped = set(), []
    for name in names:
        if name in GENERIC:
            skipped.append(name)
            continue
        for f in files_mentioning(name, head, path):
            if f in changed or not os.path.isfile(f):
                continue
            text = read(f)
            if name == stem:
                ok = any(not clause.lstrip().startswith("{") and resolve(spec, f, changed) == path
                         for clause, spec in IMPORT_STATEMENT_RE.findall(text))
            else:
                ok = any(reexports(resolve(s, f, changed), path, changed) for s in MODULE_SPEC_RE.findall(text))
            if ok:
                found.add(f)
    return sorted(found), skipped
