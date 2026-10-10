# Consolidated engineering rules

Union of market-clean (MC), nn-chrome-extension (NN), tomapan (TP). Strictest wins where they differ.

## File & module structure

- Hard cap **300 lines per non-test file** (MC: build gate; NN: ESLint `max-lines` warn). New files target **≤200** (TP PR self-check).
- Tiered guidance (TP): screens ~300, components ~150–200, hooks ~100–150, pure modules ~200–300. Hit limits by extracting concerns, not artificial wrapping.
- **Preflight line counts** on files you expect to touch before coding; if a target is over cap, split it in the first implementation pass (MC). Don't preemptively refactor an over-cap file you're not touching (NN).
- Extraction order when splitting (TP): pure helpers → shared types → sub-components → data/effect hooks → sibling `*.styles.*` file.
- **No barrel files / re-export facades**; import from the defining module; repoint consumers when you split (NN).
- Feature-based folders over type-based (MC). One orchestrator + focused helper modules (MC).
- **Pure logic separated from side-effect/DOM/IO layers** — the pure halves are the unit-tested ones (MC, TP).
- Shared constants live in one constants module; **no magic strings for any identifier used in more than one place or crossing a system boundary** (TP, MC).
- No circular imports. Import ordering: builtin → external → internal alias → relative, blank line between groups, alphabetized (NN, TP).
- Layering (TP): each layer imports only from layers below; UI never imported by domain. Unsure where code goes: touches React state → hook; otherwise → pure module.

## Comments

- **Hard cap 2 lines, prefer ≤1** (MC memory — strongest rule). NN: max one line.
- Only the non-obvious **why**; the code shows what. Delete self-explanatory comments.
- **Never narrate the change/session** or justify choices to a reviewer in comments.
- Keep pre-existing incident-rationale comments during cleanups (MC).
- Re-read and line-count every comment before finishing a turn (MC).
- TODOs carry a task/issue reference (TP).

## TypeScript / language

- Strict mode + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` (TP).
- No `any` without an escape-hatch comment explaining why (TP `// @agent-allowed: any because …`).
- **`unknown`-first parsing** of external/stored payloads; almost no casts (NN).
- Typed domain errors; never throw plain strings; pure modules return results instead of throwing (TP).
- No dead code on main: delete, never comment out; no `console.log` in committed code (TP). Remove only orphans *your* change created; mention pre-existing dead code instead of deleting unasked (Karpathy).
- Don't add another flavor of an existing helper — reuse the right one (NN). Don't imitate existing bad patterns (NN).

## Testing

- **Every feature/fix ships with its automated test(s)** (MC paid-product bar). Bugs get a reproducing test first (TP TDD).
- **Two tiers**: (A) deterministic, credential-free, CI-safe; (B) live against reality, env-gated, local-only, never CI (MC, NN). Release gate runs both, **fails closed** if the live env is unavailable (MC).
- Never test a copied fixture of the source — load the real module and inject dependencies (MC).
- Fixtures are **structural/semantic — never the host site's rotating class names** (MC).
- Never weaken/skip a release-blocking test to pass; park unmet requirements as explicit `test.fixme` with measured evidence (MC).
- **Measure, don't assume**: quantify perceived behavior before/after and keep the measurement as the test's budget (MC).
- No UI snapshot tests (TP). Table-driven tests for multi-case functions; seeded determinism, no `Math.random()` in tests (TP).
- Never answer a user-visible defect with "the tests pass" — if the suite is green and the user sees a bug, the test's reference frame is wrong: fix the test first (NN).
- "A build is not your source": rebuild before re-testing after reverts — stale bundles lie (NN).
- Data-layer modules take injected clients/collections so they unit-test without the real DB (MC).

## Workflow & session

- **Agent never runs git** (add/commit/push/checkout/merge) and never deploys/publishes — the human owns git and releases. Leave changes as working-tree edits and hand over exact commands (MC memory, NN, TP). No AI-attribution trailers in commit messages (MC memory).
- One concern per change; never expand scope; no adjacent refactors "while you're there" (NN, TP, Karpathy).
- Read the project's guidance docs before coding (all three). Session start: AGENTS.md → README → PROGRESS.md.
- **DoD**: typecheck + lint + tests green before declaring done; list every file touched (NN, TP). Mechanize the gate in a review script: syntax check, run tests, line-budget check, invariant greps (MC `review-after-feature.sh`).
- Ask, don't assume: stop on ambiguity that changes the result; present interpretations instead of silently picking (TP, Karpathy).
- Convert tasks into verifiable goals with per-step checks (Karpathy).
- Zero live-user impact as a standing default once shipped: behavior-preserving on hot paths or fully dormant; additive over modifying (MC memory).

## Docs

- Docs are source of truth: if code and docs disagree, update docs in the same change or stop and ask (TP).
- **`## Regression guards` section** in the README: every non-obvious behavioral fix recorded with the incident and "do not remove this guard" (MC).
- **Record dead ends** with evidence — what was tried, measured, why removed, "do not rebuild without new evidence" (MC).
- Never describe/market features that aren't implemented; verify every behavioral claim in code before writing user-facing copy (MC memory).
- Verify third-party API shapes against **live docs** for the account's actual API version, never from memory (MC memory).
- PROGRESS.md is the decision log: dated entries under `## Deferred decisions`, `## Rejected decisions` (with reason), `## Open questions`. Prune completed work; history lives in git (TP TASKS.md pattern).

## UI

- **Design tokens only** — no raw colors/radii/shadows in components; add the token first, then consume it (MC DESIGN-SYSTEM, TP).
- A11y baseline: visible focus on all focusable controls, legible in light + dark, never remove labels (MC).
- All user-facing strings through i18n, keys aligned across locales (TP, MC).
- Stable interactive element IDs — they are a contract with the logic (MC).
- Clean, minimal, functional; disabled controls look disabled and don't animate; show controls only when they can affect something (MC).

## Browser-extension discipline (include only for extension projects)

- **Never depend on the host's obfuscated/generated class names** — they rotate. Anchor to persistent semantics: visible text, structure, `role`, aria, `data-*`, href patterns, currency symbols (MC).
- **Confidence scoring over hard gates** for element identification: weighted soft signals with a threshold (MC).
- **Read-only toward the host**: never automate clicks/messages/posts, never intercept its network, never scrape beyond what the user sees; observe and modify only your own overlay state (MC, NN).
- **Never restructure the host's DOM**: no reparenting, no hiding its sentinels; clear every injected marker when a node is recycled or the feature is disabled (MC).
- **Single evaluation pipeline** for initial scan and dynamically-added items — no separate branches (MC).
- **One MutationObserver on the root**, dedupe added subtrees, **batch per animation frame** (hide/annotate before paint), never polling as the main mechanism (MC).
- **Per-item fault isolation**: try/catch around the per-element operation, count, continue — one malformed item never aborts the pass (MC).
- Graceful degradation: if detection fails, log and skip; never act on an unresolved element (MC).
- **Duplicate-injection guard** in every entry-point script; error-checking within a few lines of every async platform call (MC review script).
- **Least-privilege permissions**, each one justified in docs; never widen host permissions for a papercut — it disables the extension until re-accepted (MC).
- Minimal egress by **explicit documented allowlist** of exact payloads (MC).
- Client-side gating is cosmetic — the server is the gate for anything paid (MC).
- Scope text extraction to the element subtree, never full-page text (MC).
- Eager, synchronous mount for content-script UI — runtime `import()` fails on strict-CSP sites (NN). No CDN assets; self-host everything (NN).
- Don't use secure-context-only APIs (`crypto.randomUUID`) in code that can run on plain http (NN).
- Settings changes apply without a page reload (MC).
- Live testing against a real site must scroll deep (10+ steps, settle waits, union by item id) — the first viewport is never representative (MC memory).
