"""Rule routing: which rules a hunk should be checked against, and the rule groups the agents split on.

Detection uses file kind and hunk content only, never project paths or library names.
"""
import re

ROUTE_EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".php", ".py", ".rb",
             ".go", ".sql", ".graphql", ".gql", ".css", ".scss", ".less")
NO_CHECK = re.compile(r"\.test\.|\.spec\.|(^|/)(tests?|__tests__|translations|locales|i18n)/")

# (label, path regex, hunk regex, rules); rows starting `^\+` only hit added lines.
CATEGORIES = [
    ("migration", r"(^|/)migrations?/|\.sql$", None, ["migrations", "scope-and-rollout"]),
    ("migration", None, r"(?i)^\+.*\b(alter|create|drop)\s+(table|index)\b", ["migrations", "scope-and-rollout"]),
    ("api-schema", r"\.(graphql|gql)$", None, ["api-layer-conventions"]),
    ("api-schema", None, r"\bgql`|\btypeDefs\b|\bresolvers?\b|\b(args|fields)\s*:", ["api-layer-conventions"]),
    ("api-handler", None,
     r"^\+.*(\b(req|request)\.(body|query|params)\b|\bfunction\s+handler\b|\bexports\.handler\b"
     r"|\b(app|router)\.(get|post|put|patch|delete)\(|\bnew Response\(|\bres\.(status|json|send)\()",
     ["api-layer-conventions"]),
    ("untrusted-input", None,
     r"^\+.*(\bargs\.\w|\b(req|request)\.(body|query|params|headers)\b|searchParams\.get\(|JSON\.parse\("
     r"|\$_(GET|POST|REQUEST)|process\.argv|location\.(search|hash)|\bpostMessage\(|\.on[Mm]essage\b)",
     ["security-access"]),
    ("api-message", None, r"^\+.*\b(message|error)\s*:\s*['\"`]", ["i18n-identifiers"]),
    ("logging", None, r"^\+.*(\bconsole\.\w+\(|\blogger\.\w+\(|\blog(Error)?\()", ["logging"]),
    ("error-handling", None, r"^\+.*(\bcatch\s*[({]|\.catch\()", ["logging"]),
    ("handler", None,
     r"^\+.*(\bfunction\s+handler\b|\bexports\.handler\b|\bnew Worker\(|\bprocess\.on\(|\bchrome\.runtime\.)",
     ["resource-lifecycle"]),
    ("resources", None,
     r"^\+.*(createObjectURL|addEventListener|setTimeout|setInterval|requestAnimationFrame|new \w*Client\("
     r"|new (WebSocket|EventSource|AbortController|IntersectionObserver|ResizeObserver|MutationObserver)\()",
     ["resource-lifecycle"]),
    ("ui-component", r"\.(tsx|jsx|vue|svelte)$", None, ["react-patterns", "i18n-identifiers", "magic-values"]),
    ("ui-component", None, r"^\+.*(</\w|/>)", ["react-patterns", "i18n-identifiers", "magic-values"]),
    ("styling", r"\.(css|scss|less)$", None, ["project-building-blocks", "magic-values"]),
    ("styling", None, r"^\+.*(\bstyle=\{\{|\bclassName=|#[0-9a-fA-F]{3,8}\b|\b\d+px\b|\brgba?\(|\btheme\.)",
     ["project-building-blocks"]),
    ("ui-hook", r"(^|/)use[A-Z]\w*\.\w+$", None, ["react-patterns"]),
    ("ui-hook", None, r"\buse(State|Effect|LayoutEffect|Memo|Callback|Ref|Reducer|Context)\(", ["react-patterns"]),
    ("state", r"(^|/)(reducers?|selectors?|stores?|slices?|state|models)/", None, ["state-and-data-flow"]),
    ("state", None, r"^\+.*(\bdispatch\(|\bsetState\(|\buse\w*Store\(|\bselect\w*\(state\b)",
     ["state-and-data-flow"]),
    ("constants", r"(^|/)(constants?|presets)(/|\.\w+$)", None, ["i18n-identifiers", "magic-values", "file-placement"]),
    ("helpers", r"(^|/)(helpers|utils?)/", None, ["file-placement"]),
    ("lint-disable", None,
     r"^\+.*(eslint-disable|@ts-ignore|@ts-expect-error|@ts-nocheck|biome-ignore|prettier-ignore|\bnoqa\b"
     r"|pylint:\s*disable|type:\s*ignore|rubocop:disable|//\s*nolint|@phpstan-ignore|@SuppressWarnings)",
     ["no-lint-disable"]),
]

# (name, rules, routed): an unrouted group reviews every hunk.
GROUPS = [
    ("correctness", ["security-access"], False),
    ("existence", ["justify-this-code", "delete-dont-keep", "reuse-before-adding", "single-use-helper-inline"], False),
    ("form", ["simpler-form", "weak-types", "naming", "magic-values", "pass-only-whats-needed"], False),
    ("ui", ["react-patterns", "project-building-blocks", "state-and-data-flow", "i18n-identifiers"], True),
    ("backend", ["migrations", "logging", "resource-lifecycle", "api-layer-conventions"], True),
    ("structure", ["comment-the-why", "file-placement", "one-convention-per-file", "logic-at-the-right-level",
                   "no-lint-disable", "scope-and-rollout"], False),
]

_COMPILED = [(label, path and re.compile(path), hunk and re.compile(hunk, re.M), rules)
             for label, path, hunk, rules in CATEGORIES]


def categorize(path, hunk):
    """Labels and rules routed to one hunk (header and context lines included in the match)."""
    if NO_CHECK.search(path) or not path.endswith(ROUTE_EXT):
        return [], []
    labels, rules = [], []
    for label, path_re, hunk_re, row_rules in _COMPILED:
        if (path_re is None or path_re.search(path)) and (hunk_re is None or hunk_re.search(hunk)):
            labels += [label] if label not in labels else []
            rules += [r for r in row_rules if r not in rules]
    return labels, rules


def groups(rule_names=()):
    """GROUPS plus an unrouted "other" group for rule files no group knows."""
    known = {r for _, rules, _ in GROUPS for r in rules}
    other = sorted(set(rule_names) - known)
    return GROUPS + ([("other", other, False)] if other else [])
