"""Contracts of the reviewer scripts on neutral fixtures. Run: python3 -B test_walkthrough.py (prints ok)."""
import io
import os
import re
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = os.path.join(HERE, "..", "rules")
sys.path.insert(0, HERE)

FIXTURES = {
    "src/orders/format.js": "function formatOrder(order) {\n  return order.id;\n}\nmodule.exports = { formatOrder };\n",
    "src/orders/list.js": "const { formatOrder } = require('./format');\nformatOrder({ id: 1 });\n",
    "src/sessions/close.js": "export const closeSessions = async () => {};\n",
    "config/functions.json": '{ "handler": "src/sessions/close.closeSessions" }\n',
    "src/cart/total.ts": "export const cartTotal = (items: number[]) => items.length;\n",
    "src/cart/total.test.ts": "import { cartTotal } from './total';\ncartTotal([]);\n",
    "src/cart/math.ts": "const double = (n: number) => n * 2;\nexport const quad = (n: number) => double(n) * 2;\n"
                        "export const neverUsed = 1;\n",
    "src/cart/CartPanel.tsx": "import { quad } from './math';\nexport default function CartPanel() {\n"
                              "  return <div>{quad(2)}</div>;\n}\n",
    "src/cart/tiny.ts": "export default function tinyThing() {\n  return 1;\n}\n",
}


def run(*args):
    subprocess.run(args, check=True, capture_output=True)


def make_repo(root):
    os.chdir(root)
    run("git", "init", "-q")
    ident = ["-c", "user.name=test", "-c", "user.email=test@example.com"]
    with open("README.md", "w") as f:
        f.write("fixture\n")
    run("git", "add", "-A")
    run("git", *ident, "commit", "-q", "-m", "base")
    for path, text in FIXTURES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
    run("git", "add", "-A")
    run("git", *ident, "commit", "-q", "-m", "head")


def facts_for(path):
    from facts import fact_checks
    from gitutil import git
    return fact_checks(path, "HEAD", git("diff", "HEAD~1..HEAD", "--", path))


def test_facts():
    assert not any("one-caller" in n for n in facts_for("src/orders/format.js")), "module.exports export missed"
    assert facts_for("src/sessions/close.js") == [], "a JSON config use must count"
    assert facts_for("src/cart/total.ts") == [], "a test import must count"
    notes = " ".join(facts_for("src/cart/math.ts"))
    assert "[one-caller] `double`" in notes and "[unused-export] `neverUsed`" in notes, notes
    assert "quad" not in notes, notes
    assert not any("tinyThing" in n for n in facts_for("src/cart/tiny.ts")), "default exports are not named"


def test_span():
    from walkthrough import span
    assert span("@@ -1,2 +10,3 @@ f\n a\n+b\n-c\n+d") == (12, 2, 1)


def test_walkthrough_document(tmp):
    import walkthrough
    out = os.path.join(tmp, "walkthrough.md")
    with redirect_stdout(io.StringIO()):
        walkthrough.main(["--base", "HEAD~1", "--head", "HEAD", "-o", out])
    doc = open(out).read()
    assert "## Groups" in doc and "### H1. `" in doc and "## Tests in this diff" in doc, doc
    order = re.findall(r"^## \d+\. `([^`]+)`", doc, re.M)
    assert order.index("src/cart/CartPanel.tsx") < order.index("src/cart/math.ts"), order


def test_round_numbers(tmp):
    from prep import next_round, undecided
    folder = os.path.join(tmp, "findings")
    os.makedirs(folder)
    for name in ("feature-cart-2026-01-01-r1.md", "feature-cart-2026-01-02-r2.md",
                 "feature-cart-panel-2026-01-03-r5.md"):
        open(os.path.join(folder, name), "w").close()
    assert next_round(folder, "feature-cart") == 3
    assert next_round(folder, "feature-cart-panel") == 6
    assert next_round(folder, "feature") == 1
    path = os.path.join(folder, "feature-cart-2026-01-02-r2.md")
    with open(path, "w") as f:
        f.write("- **2.A1. `src/cart/math.ts:1`** — **Unused.** x\n  - [x] request change — **author:** fixed\n"
                "  - [ ] not now\n- **2.B1. `src/cart/total.ts:1`** — **Question.** y\n"
                "  - [x] request change — **verify:** holds — z\n")
    assert undecided(path) == ["2.B1"]


def test_groups():
    from routing import CATEGORIES, GROUPS
    assert os.path.isdir(RULES), f"rules dir missing: {RULES}"
    files = sorted(n[:-3] for n in os.listdir(RULES) if n.endswith(".md") and n != "_do-not-flag.md")
    grouped = sorted(r for _, rules, _ in GROUPS for r in rules)
    assert grouped == files, (f"groups {len(grouped)} vs rule files {len(files)}; "
                              f"difference: {sorted(set(grouped) ^ set(files))}; repeated: "
                              f"{sorted({r for r in grouped if grouped.count(r) > 1})}")
    routed = {r for _, _, _, rules in CATEGORIES for r in rules}
    for name, rules, is_routed in GROUPS:
        missing = [r for r in rules if is_routed and r not in routed]
        assert not missing, f"group {name}: {missing} in no CATEGORIES row"


def main():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "repo")
        os.makedirs(repo)
        try:
            make_repo(repo)
            test_facts()
            test_span()
            test_walkthrough_document(tmp)
            test_round_numbers(tmp)
        finally:
            os.chdir(cwd)
    test_groups()
    print("ok")


if __name__ == "__main__":
    main()
