# Consolidated engineering rules

Union of market-clean (MC), nn-chrome-extension (NN), tomapan (TP), make it accessible (MIA). Strictest wins where they differ.

## File & module structure

- Comments everywhere: max 2 lines, prefer 1 (founder decision 2026-10-22); a project may keep a stricter 1-line rule (NN, TP).
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
- **Types are defined, never asserted**: no `as` (except `as const`), no non-null `!`, no `any`; ESLint `consistent-type-assertions: never` + `strictTypeChecked` (MIA).
- **zod at every boundary** (files, network, model output, CLI events); types inferred from the schema, never written twice. Size limits go after parsing, not in the schema (MIA).
- Node-run TypeScript: **erasable syntax only** (no `enum`, parameter properties, namespaces); `verbatimModuleSyntax`, `allowImportingTsExtensions`, `noEmit` (MIA).
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
- A green check on an empty project proves nothing: say what it covered (0 packages, 0 tests) (2026-10-22).
- A negative lint/type test asserts the rule ID that fired, not only a non-zero exit (2026-10-22).
- Size a rule by diffing old against new outputs, with the rule's own predicates in the probe; a hand-written count is no baseline. An acceptance criterion's "allowed diff" is checked against the baseline first; a cap raise needs an input that hits the cap (MIA).
- A reference drawn by the same code as the output shares its bugs: verify against an independent source (MIA, 2026-10-24).
- Run a regex built from one sample over every input it will see; a heuristic acceptance window fires on ordinary data too: measure its share (MIA).
- Tests of a dedupe pass two distinct inputs sharing a key, not one input twice; "every match satisfies P" is true on none (require one); folding `!a && !b` into `a >= b*k` turns 0/0 into true (MIA).
- Name a count by the unit it counts; an "unmatched" count is the failures inside the loop that tried, never candidates minus successes (MIA).
- Nondeterminism: hash every byte at production size with enough runs to beat the flip rate, set tolerances over all pairs at the resolution the noise was measured at, and count a flag as a fix only if the output bytes change (MIA, 2026-10-24).

## Tooling

- **One `check` command** = typecheck + lint + format check + tests; it is the definition of done (MIA).
- Exact-pinned dev dependencies installed at init time, never hard-coded versions in a template (MIA).
- "Latest" is not one version set: pin each tool to a combination whose peer ranges agree (TS 7 vs typescript-eslint `<6.1`, 2026-10-22); `pnpm peers check` clean.
- A reference project's process generalizes; its toolchain only to projects on the same runtime (Node-native TS does not run in a browser) (2026-10-22).
- max-lines counts test files, and Prettier wraps long lines into several: count after formatting. Scripted edits anchor on function names or comment lines, never long expressions Prettier reflows (MIA).
- A here-doc `cat > file` with nothing to read blocks on stdin; a `ps | grep` wait loop can match itself (MIA).
- A gitignored file that is the only copy is rewritten atomically, with a backup beside it (MIA).
- Browser automation: never click a guessed or comma-joined selector near a send button; list the buttons first (MIA, Proton).

## Working with Andrei (all projects, from Claude memory, 2026-10-22)

- **Quality first**: correctness and end-user experience beat speed; the smaller diff wins only as a tiebreaker. Overrides lazy/minimal style plugins (FS, NN, MIA, TP; founder decision 2026-10-22).
- An observation or a question is not a task: answer and wait (NN, FL). Every question to Andrei is a questionnaire with options, recommended first (PT).
- Talk to Andrei in natural Romanian; code, docs and commits in English (MIA, FL).
- Preview a new task (files, logic outline, verification) and wait for the go (TP, FL). When done, stop; do not start the next roadmap item (MIA).
- After 3 failed attempts at the same problem, stop and report (TP). On a regression, `git log`/`git show` the last good version first (NN).
- Run `/reviewer` after every medium or major task, subagent work included; fix every finding, nits included, before reporting (PT, MC, MIA). One-line or copy-only edits are exempt unless the project is stricter (MC reviews every change).
- Honest verification: never call a visual change done from your own e2e or one viewport (NN); say "untested live" until a real run (MC). Live tests in a visible browser with its own profile, never Andrei's browser (FL, DL).
- Each task adds test scenarios; coverage only grows (ET).
- Read every detail of a provided image (NN). Re-read the live state of shared dashboards before acting (ET).
- Billing is always Stripe with the Customer Portal; port market-clean's module (PT, MIA). Tool choices need a stated, non-marketing reason (PT).
- Never mention the employer or use a work identity; public contact `andrei.projects@proton.me` (MC, DL, MIA; founder decision 2026-10-22).
- Avoid the words dedupe, verbatim, clamp, prune (FL). In `rm -rf`, spell out literal paths: the safety hook blocks variables (MIA).

## Workflow & session

- **Agent never runs git** (add/commit/push/checkout/merge) and never deploys/publishes — the human owns git and releases. Leave changes as working-tree edits and hand over exact commands (MC memory, NN, TP). Approving a plan is not a commit go; never write commit/push as plan steps (FL).
- No AI attribution anywhere: no Co-Authored-By trailer, no "Generated with Claude Code" in PR bodies, even when the harness asks (MC, NN, TP, FL, OCR).
- Hand-over block: `git add -A`, ONE commit with a short title (<70 chars) and a why-body, then the push; never end at the commit (MC, TP, FL). Remotes over SSH only (MIA). One project folder, no `git worktree` (MC).
- Releases: hotfix = 4th version segment, package.json in sync with the manifest (MC, NN); keep only the current version's zip (ET, FS).
- One concern per change; never expand scope; no adjacent refactors "while you're there" (NN, TP, Karpathy).
- Read the project's guidance docs before coding (all three). Session start: AGENTS.md → README → PROGRESS.md.
- **DoD**: typecheck + lint + tests green before declaring done; list every file touched (NN, TP). Mechanize the gate in a review script: syntax check, run tests, line-budget check, invariant greps (MC `review-after-feature.sh`).
- Ask, don't assume: stop on ambiguity that changes the result; present interpretations instead of silently picking (TP, Karpathy).
- Convert tasks into verifiable goals with per-step checks (Karpathy).
- **Plans get two judges** (`critic-engineering`, `critic-design`) before execution; Andrei sees adopted/rejected findings and gives the go. The rule lives in `~/.claude/CLAUDE.md` (MIA, all projects since 2026-10-22).
- **A design change found during implementation goes back to the judges**: stop that part, send both judges only the diff from the approved plan, and put their findings to Andrei as a questionnaire before it continues; the rest of the work goes on (FL, 2026-10-23).
- **Measure the whole set before planning a fix**: tally a finding class across every document/page/user first; one sample is not a rate (MIA).
- Judges get the user's request verbatim and a fresh context; a judge that only sees the plan cannot catch a misread intent (2026-10-22).
- Zero live-user impact as a standing default once shipped: behavior-preserving on hot paths or fully dormant; additive over modifying (MC memory).

## Docs

- Docs are source of truth: if code and docs disagree, update docs in the same change or stop and ask (TP). Trim rather than append; aim for a net line reduction (TP).
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
- Positional CSS (`nth-child`) breaks when an optional element is missing: select by class (MIA).
- Specificity: check the computed style, not the source. A class on an element coloured by a more specific rule does nothing; a pseudo-element reset must outrank what it resets; a property on a broad selector reaches every descendant (MIA).
- Custom properties inherit: a nested element writes every property it uses, or the parent writes none. Text reused outside its element (labels, aria) is the plain string (MIA).
- Client rects ignore clipping: geometry probes exclude screen-reader-only descendants. `document.fonts.ready` resolves when a face fails: check each face's status (MIA).
- VoiceOver in Safari stops on every block or inline-block child: `role="text"` joins them. Text shrunk by `clamp()` on phones needs 4.5:1 everywhere (the large-text exception is unsafe) (MIA).
- `hyphens: auto` breaks headings mid-word: `hyphens: manual` with `overflow-wrap: break-word`. Clip with `overflow: clip`, not `hidden` (find and focus scroll it); a clip on a focusable's parent clips its focus ring (MIA).
- Floors for zoomed or magnified reading are written in em, not viewport width. Chrome does not scroll a partly visible focused element and scroll-snap acts only after a scroll: probe such fixes (MIA).

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
- "Nothing happened" asserted with poll-until-match passes before the async effect lands; record the events directly, or wait a fixed settle time and assert the state is stable (Fillnote).
- A "no collision" or "not present" result needs a positive control showing the detector sees the thing it reports absent (Fillnote).
- A live safety predicate is proven in both states (false in the unsafe mode, true after the switch) and read from the control's own scope, never from page text (Fillnote).
- "Nothing posted" on a non-empty thread is measured by its item count before and after; autosave and button paths send without any Enter key (Fillnote).
- A fixture that imitates a host's behaviour hooks in where the host does (an editor plugin, not a page capture listener), and is recorded as a model, not proof; the live run is the proof (Fillnote).
- Prefer keeping input where it is until the key is released over guarding the page after the hand-off. Case: held Enter fixed in the form, not with a page listener. (Fillnote)
- Export comes before the founder starts daily use, not in a later slice. Case: Phase 3 slices 2–4 change the template format, export was slice 5. (Fillnote)
- Waiting for a key's release also ends on the modifier's keyup and on window blur: macOS drops a key's keyup while Cmd is held, and a short cap hides that. Case: `KEYUP_WAIT_MS` with Cmd+Enter. (Fillnote)
- Pass/fail thresholds for a decision rule (audience swap) are fixed before the run, deviations named there. Case: spike (c) H3 with undo grouping left open. (Fillnote)
- An html renderer keeps meaningful spaces (run edges, repeated spaces) as &nbsp;: rich editors parse pasted html with whitespace collapsing (Fillnote).
- Before claiming a live test covers a new code path, check it calls that path rather than a hand-built payload (Fillnote).
- Isolated-world error capture in a shared browser profile keeps only our extension's context id; "first `chrome-extension://` world" can be another extension's. Case: `proveErrorCapture` in the live profile with LastPass. (Fillnote)
- A live target must be the surface named in the plan, not a nearby editor in the same product. Case: HubSpot contact "Create a Note" standing in for the "HubSpot inbox". (Fillnote)
- A component that keeps an invalid state to itself makes its parent save the last valid value; it reports the invalid state through the same callback (Fillnote).
- A page that reads data written by another context uses the writer's own parser, so both agree on what counts as unreadable (Fillnote).
- Making a field optional is judged against the features that exist today (Fillnote).
- A form that writes through a message channel has copy for "no reply" as well as for every error code (Fillnote).

- Sign-in inside `launchWebAuthFlow` cannot depend on a link opened elsewhere (magic link); use a one-time code or OAuth in the same window. Case: plan/06 extension auth. (moved from Fillnote critics, 2026-10-24)
- In a churn model, 1/churn months reaches only ~63% of steady state; size acquisition for the actual deadline. Case: plan/07 understated installs needed by ~30%. (moved from Fillnote critics, 2026-10-24)
- Vite lib mode is for libraries, not extension entry points: use non-lib `format: 'iife'` builds with `emptyOutDir: false`. Case: Fillnote scaffold `build.ts`. (moved from Fillnote critics, 2026-10-24)
- A hypothesis's success threshold must come from the plan's own economic model. Case: H4 counted 1,500 installs/month as success, which projected ~$165 MRR. (moved from Fillnote critics, 2026-10-24)
- A differentiator headline must not be a feature the plan's own comparison table credits to the leader. Case: "preview before insert", already present in Text Blaze and TextExpander. (moved from Fillnote critics, 2026-10-24)
- Every site named in listing or homepage copy must be in the tested tier. Case: Zendesk named in plan/03 while Tier 2 in plan/04. (moved from Fillnote critics, 2026-10-24)
- A scaffold asked for as "phase N" tracks phase N's deliverables, not the next phase's backlog. Case: Phase 2 request, ROADMAP pointing at Phase 3. (moved from Fillnote critics, 2026-10-24)
- Every question to the founder carries a recommended default and the point where it becomes irreversible; engineering risks are not founder questions. Case: gecko id, TSX runtime. (moved from Fillnote critics, 2026-10-24)
- Version-based sync must compare the client's base version (compare-and-swap), never "client version is greater". Case: plan/06 lost an edit when the other device had edited more times. (moved from Fillnote critics, 2026-10-24)
- A store source archive built with `git archive HEAD` ships the whole repo; scope it by path. Case: Fillnote `zip.ts` would have sent plan/ to AMO. (moved from Fillnote critics, 2026-10-24)
- Production evidence must match the exact usage form (callbacks vs promises) before it justifies an API choice. Case: market-clean's callback-only `chrome.*` cited for promise calls. (moved from Fillnote critics, 2026-10-24)
- A rule making product docs read-only must allow the edits the plan's own acceptance criteria require. Case: plan/09 Phase 2 updates the Tier lists in 04. (moved from Fillnote critics, 2026-10-25)
- Fixture evidence may demote a Tier 1 site but never confirm one; live-unvisited sites are reported as "untested live". Case: spike (b) would have confirmed WhatsApp, Discord, X, ChatGPT and Salesforce from fixtures alone. (moved from Fillnote critics, 2026-10-25)
- Test payloads include the hardest real shape (multi-line, list, link), not only a one-liner. Case: spike (b)'s single-line payload skipped the paragraph and Enter-to-send risks. (moved from Fillnote critics, 2026-10-25)
- Setting a DOM selection and dispatching a synthetic event in the same task reaches model editors with a stale selection; wait for `selectionchange` or pass `targetRanges`. Case: ProseMirror `doPaste`, slate-react throttle. (moved from Fillnote critics, 2026-10-25)
- Expandos set by page code (`__quill`, React fibers) are invisible from an isolated-world content script; detect from the DOM. Case: spike (b) Quill version check. (moved from Fillnote critics, 2026-10-25)
- An undo assertion after a synthetic edit depends on the editor's history merge delay; pin the timing in the test. Case: Quill 1000 ms, ProseMirror 500 ms. (moved from Fillnote critics, 2026-10-25)
- Live-site evidence is cropped to the element under test and kept out of git; real accounts never message a third party. Case: Gmail and LinkedIn screenshots and drafts in spike (b). (moved from Fillnote critics, 2026-10-25)
- A trigger that acts on an async reply re-checks its precondition when the reply lands, and a test types into the gap. Case: spike (d) background render vs fast typing. (moved from Fillnote critics, 2026-10-25)
- IME support covers what the IME commits (full-width `；`), not only composition events. Case: spike (d) T2/T3. (moved from Fillnote critics, 2026-10-25)
- A trigger built only on `input` misses editors that cancel `beforeinput` and render themselves; test shortcuts ending in digits and punctuation. Case: slate-react inserts natively only for `/[a-z ]/i`. (moved from Fillnote critics, 2026-10-25)
- A passing size budget does not prove a dependency was tree-shaken; keep the import out or assert its absence. Case: full zod at 24.5 KB passes a 30 KB budget. (moved from Fillnote critics, 2026-10-25)
- `chrome.storage.onChanged` has no key filter: every listening frame receives every change with its value. Case: plan/06 claimed watching only `index` keeps template saves out of tabs. (moved from Fillnote critics, 2026-10-25)

- 2026-10-23 — A guard is tested with the input that defeats it, typed per key as users do, not only with Playwright `fill` (one insertText). Case: spike (d) `endsWith(data)` deferred-scan guard.
- 2026-10-23 — A "user acted" detector ignores modifier-only keys, and its test uses a key that changes neither text nor selection, or the test passes without the guard. Case: spike (d) `watchUser`; ArrowRight and Lexical keys passed vacuously.
- 2026-10-23 — Latency for an occasional action is reported in the state users meet it (cold service worker), warm second. Case: spike (d) T6.
- 2026-10-23 — An insertion result keeps "the user took over" apart from "the editor failed", so the UI never presents a deliberate undo as a site failure. Case: spike (d) undo → `unverified` → "Copy result"; the distinct reason lands with spike (f).
- 2026-10-23 — When implementation reverses a regression guard, the README guard is rewritten and the old approach goes to Dead ends in the same change. Case: README still said to wait for `selectionchange` after the synthetic dispatch replaced the wait.

- 2026-10-23 — A race fix proven only by a test failing 1 time in 3 needs a deterministic test before its mutation check means anything. Case: spike (d) T1 undo in Draft.js and Slate.
- 2026-10-23 — A selection made only for an insertion is made and used in one task: dispatch a synthetic `selectionchange`; never wait for the native one, because a typed key replaces the selection. This replaces the "wait for `selectionchange`" half of the 2026-10-22 entry. Case: spike (d) T7, `Before xBest regards`.
- 2026-10-23 — Verifying an insertion by its suffix alone passes when the editor inserted at a stale caret; also check the trigger text is gone. Case: `;sigBest regards` passed `endsWithText`.
- 2026-10-23 — "Leaves the page as it was" includes scroll position and the page changing underneath. Case: spike (f) F3 checked only text and caret.
- 2026-10-23 — A focus hand-off is tested across the key's whole life (keydown, keyup, auto-repeat), not keydown alone. Case: spike (f) F6 counted Enter keydowns only.
- 2026-10-23 — A wait one editor needs is scoped to that editor; a global delay hands its failure mode to every family. Case: spike (f) one-frame wait for Draft.js would have opened an Enter-to-send gap in WhatsApp and Discord.

- 2026-10-23 — UI injected outside an open modal is inert under `showModal()`, and focus traps pull focus back; mount it inside the active modal and test with one. Case: spike (f) host on `documentElement`.
- 2026-10-23 — A "show only when focused" gate also needs a "close when focus leaves" rule; the opening gate alone does not keep keys out of the page. Case: spike (f) step 5.
- 2026-10-23 — Refocusing a React-controlled editor schedules a re-render (a microtask under `createRoot`), and a selection set in that task is dropped; insert one frame after the refocus. Case: spike (f) Draft.js `Before ;formHi Alex.`.
- 2026-10-23 — After the user has filled a form, "the user's typing wins" must not silently throw the form away; the values stay recoverable. Case: spike (f) skipped insertion drops the form; Phase 3 Copy result covers it.
- 2026-10-23 — A native-element fixture does not stand in for its ARIA lookalike; test both. Case: spike (f) `showModal()` vs `div[aria-modal]` helpdesk modals.
- 2026-10-23 — When one mechanism covers a case, that mechanism gets the mutation check. Case: the top-layer popover had none until a max z-index fixture pinned it.

- 2026-10-23 — `new URL(u).origin` is "null" for `chrome-extension:` URLs, and `use_dynamic_url` frames keep the `chrome-extension://<id>` origin; build a `postMessage` target from `chrome.runtime.id`. Case: spike (f) init dropped silently.
- 2026-10-23 — A guard is shown unnecessary only against the strongest real case, with the real library where one exists. Case: spike (f) dropped the modal mount on two trap styles; react-focus-lock (crossFrame on, Jira, Chakra) then failed every test without it.
- 2026-10-23 — A claim that the UI "cannot create" a shape is checked against every keymap and paste path, not only the toolbar. Case: spike (h) bound Tab to `sinkListItem` and allowed bold inside links.
- 2026-10-23 — Data an editor creates outside its undo history needs an undo and delete rule with a test. Case: spike (h) field definitions outlived an undone chip.
- 2026-10-23 — An inline element set apart only by fill colour needs a border or shape. Case: chip #ECE8FC on white is 1.2:1 and vanishes in forced colours.
- 2026-10-26 — Before writing "still rejects X" in a plan, run the current predicate on X. Case: a regex plan claimed "2/5" failed; it already passed.
- 2026-10-26 — Relaxing a check shared by several regex branches widens every branch: relax it only where the case needs it. Case: a "never falling" sizes rule would have let "$12/12" and "5/5" pass.
- 2026-10-26 — A test of a unit conversion uses a scale ≠ 1, or px and pt mixed up pass. Case: Make It Accessible scan areas (image px × points per px).
- 2026-10-27 — A store text limit is checked by counting the exact proposed string (`wc -c`), never by eye. Case: a 134-character Chrome summary against a 132 limit.
- 2026-10-27 — Splitting a CI job into a matrix: check what the old single command built implicitly, and give every uploaded artifact a per-leg name. Case: `e2e:<browser>` skipped the extension build; upload-artifact v4 rejects duplicate names.
- 2026-10-27 — A test-driver workaround for a hang names the user-visible effect it rules out and asserts it (the next key lands). Case: leaving a lost keyup pending once the overlay closed.
- 2026-10-27 — An identifier sent before consent is data collection: phone home only when a feature the user chose needs it. Case: install registration on first run vs "stays on this device".
- 2026-10-27 — A consent default is checked against the legal basis the privacy page already states. Case: Chrome analytics opt-out vs "only with your consent".
- 2026-10-27 — Placing serverless functions in an existing hosting project starts by checking its root directory, deploy method and routing flags (`trailingSlash`, `cleanUrls` redirect API paths and break preflights and webhooks). Case: the WriteOnce API in the static site's Vercel project.
- 2026-10-27 — A Firefox extension's origin cannot be allowlisted (random `moz-extension` UUID per install): use `host_permissions` for the API origin, keep CORS as defence, the token as auth.

## From WriteOnce critics (WO, promoted 2026-10-31)

- A harness ported from another project is checked for what it rewrites and for what it never used. A live safety guard aimed at one conversation checks the exact URL and the page's own conversation id right before the risky key (WO).
- Write rules are decided on the trusted side from storage, never from the request (create vs update by a client id); a client preview of "will this work" calls the same pure function (WO).
- Before scoping a fix to one input shape, check which shapes production sends. Before a plan cites "the existing X" or today's behaviour, grep and read it; restoring a removed flow reads the removal commit's whole diff (WO).
- A mechanism with a "Do not remove" guard is changed only after citing and spiking it; deleting a spec first moves its guard cases to a surviving test. Trace where each event happens before planning "one line per call site" (WO).
- Once-only flags need a reset path when their state can be undone; cleanup after a committed write never turns the reply into a failure; a renderer fed live input never throws on partial values (`Intl` RangeError) (WO).
- Parsers tokenise only the known grammar; an importer checks the file shape once and parses each entry alone; an export escape is undone on import and round-trip tested on real values (WO).
- An edit rebuilt from a form draft merges onto the stored record; a rename separates product identifiers from external names tests match; a workspace rename is verified with `--frozen-lockfile` (WO).
- CAS data layers are tested against the real database; an idempotency record carries the change id on the row; a losing create-once CAS compares the stored value with its own; a crash-resume record redoes every later step and needs nothing they destroy (WO).
- Enumeration-safe endpoints apply every limit to known and unknown inputs before the lookup. A share of a shared provider quota is sized from every send path of every consumer. MongoDB remove-and-add on one array is one positional `$set` (WO).
- A name served by a DNS wildcard loses it once it has any record of its own: add the explicit A/ALIAS in the same change (WO outage, ~35 min).
- CI: a pipe sets pipefail and checks output size; a CLI a step relies on must still ship with the pinned runtime (corepack left Node 25); an e2e needing a service gets it in the workflow, never "skip when unset"; e2e against rate-limited endpoints counts every shared cap and seeds the rest (WO).
- Vercel functions: set `maxDuration` below any lease, count returned rows against the 4.5 MB response cap, count functions against the plan cap (Hobby 12), check the builder reads a config key; generated `.js` folders need an ESLint ignore (flat config ignores `.gitignore`) (WO).
- A dispatcher keyed by a URL segment looks names up with `Map`/`hasOwn` (no `/api/constructor/`) and is tested against the routes directory (WO).
- Stripe: count a lapse from `ended_at`, never `current_period_end`; events 409'd before their parent doc arrive later, so never write transitional states that remove access; test vs live URLs live in the deploy env behind a server redirect; an allowlist turning paid lists every gate it protects (WO).
- E2E: an entry page's URL, loading state, heading or selector attribute change greps every harness that waits on it; Playwright Chromium emulates focus (turn it off and assert `hasFocus()===false`); before removing a wait, list every key up to the next assertion; cutting tests never cuts a cited covering test (WO).
- Focus that targets a row created by a write waits for the render and handles filters that hide it. A theme or token mechanism is removed in the same phase its replacement ships (WO).
- An optional email in an anonymous collection makes it personal data. A drill names what it must prove (the backup artifact, not a fresh dump). Before any `git add -A`, check untracked files for secrets; a page script reused by a second page is checked for hard-coded navigation (WO).
- Extensions: in Firefox content scripts build events with the page's constructors (`cloneInto`); a late capture listener on `window` runs after the page's own; content-script focus listeners gate on `isTrusted`; a handler returning false gives no error code; ack before a delivery the requester won't outlive (WO).
- Extensions: per-site rules for cross-origin frames come from `sender.tab.url` (Firefox has no `ancestorOrigins`); probe which APIs a framed page has; state from `onStartup`/`onInstalled` is also checked at top level; `alarms.create` resets the period, so get first; Firefox `permissions.request` needs the gesture synchronously (WO).
- Extensions: "before paint" on an MV3 page needs a synchronous classic script from `public/`; assets reach the package only from Vite's `publicDir`; components hosted on non-extension pages get strings passed in (WO).

## Product & copy (from WriteOnce design critics, promoted 2026-10-31)

- Copy states a limit, feature or supported site only once the code and the live-test record back it; every string promising a missing feature is found and dropped, not one row (WO).
- A limit is tested at the cap, above it on edit and with an unknown id; "delete one" copy at cap + 1 and above; a quota that counts one of two ways to finish makes the other a bypass (WO).
- A state inferred from a failure, and a shared error code's copy, are true for every cause; every contract error maps to a UI state with a way out; a bridging state is walked from every way in (WO).
- Founder questions say when they depart from an approved mockup, check the recommended option against recorded decisions, come after diagnosis, and never re-ask a decision already in the docs (WO).
- A button that sends the user elsewhere is labelled with its destination; a setting that gates a feature with the feature's name; per-browser steps with each browser's own UI words (WO).
- Permission flows: spec every grant shape, check a popup survives the prompt, put the grant before the success line it makes true, re-check on the next click, spec it on every surface that accepts the opt-in (WO).
- A deletion or anonymity promise is checked against every store keyed by the value (rate-limit counters, IP keys, backups, provider logs); "fix the privacy page" audits every paragraph (WO).
- Timing copy matches the real schedule and how the platform loads config; a page-level notice says when it clears; "use defaults when invalid" fabricates a default once shown; missing and corrupt are separate states (WO).
- Purchase entries show the price before asking for anything; redirects into a third-party flow end their errors on a readable page; "Ends" and "Renews" are separate states; Pro data stays removable after a downgrade (WO).
- A whole-replace restore names what it removes and never overwrites what the user cannot see; a snapshot label says which moment it holds (WO).
- A static site with no build step has no partials: measure shared chrome against the largest page before choosing its markup; re-scope a shared stylesheet's element rules before adding chrome (WO site, 2026-11-02).
- Decorative motion over 5 s needs a pause (WCAG 2.2.2); reduced motion removes every effect tied to it (masks, the pause control); "no sideways scroll" inside `overflow:hidden` proves nothing, assert each child is in the viewport (WO site).
- A model site with one theme is copied into every theme you ship; site mocks of a product mid-redesign stay schematic and few (WO site).
- A summary of a detailed matrix (strip, badge) is checked against it and links to the detail it hides; third-party logos need the owner's licence, names in text state compatibility (WO site: Microsoft, LinkedIn, Meta rules).
- Fonts are self-hosted (Google-hosted fonts: LG München I, 3 O 17493/20); curl the host's live cache-control before adding a late-discovered subresource, and version a file given an immutable cache (WO site).
- (2026-11-02) Turning a status table into tiles or tags: map every old claim to its new place before building and carry each caveat as written, per browser and per context; merged notes lose qualifiers (who causes a behaviour, which browser).
- (2026-11-02) On a public site, a path inside the product is prefixed with the product name when a step shares its name with the site's nav ("In WriteOnce: Pricing", not "Pricing ›").
- (2026-11-02) A "not yet promised" list never borrows the confirmed state's visuals (✓, the same pill style).
- (2026-11-02) A line cap on HTML/CSS is enforced by nothing when ESLint covers only ts/tsx: state a line budget before growing a page near the cap and check it with `wc -l`.
- (2026-11-04) Before planning "one line at each call site", trace where each event happens; a result handled in a content script or frame never reaches the background. Case: slice 8 insert and family counts. Case 2026-11-04: the palette renders inside its own frame and never reaches the background `render()` named as the choke point for "every route".
- (2026-10-29) Before removing a wait, list every key between it and the next assertion; a plan that cuts tests never cuts a cited covering test and counts after earlier cuts. Case: `HISTORY_SETTLE_MS`; trigger:139 citing overlay:94.
- (2026-11-04) Before a plan says "the existing X" or cites today's behaviour, grep and read it; restoring a removed flow reads the removal commit's whole diff. Case: no `storage.onChanged`; the Conflicts filter; 474279e. A builder reused for made-up data is checked for its input type and the data claim against the data (`buildExport(Template[])`; "a Support template without fields" when all have fields).
- (2026-11-01) A global rule on an element selector (`button`, `select`) is checked against every element of that type and every older rule for it, and a page-level override matches or beats the shared rule's specificity. Case: nowrap on picker rows and `button.link`; the overlay's `.field select`; `:root` vs `:root[data-theme='dark']` color-scheme.
- (2026-10-28) A promise for a missing feature is searched in every string: a rule "until X exists" ends when X ships, a SPEC surface shipped early is audited, and a dropped Undo or deferred feature leaves no claim behind. Case: shortcut required until the palette; "Not synced yet"; "Use this version"; "recoverable with the old key".
- (2026-10-30) A plan premise about existing behaviour is checked against the e2e tests, and a design from an older snapshot against rules that loosened since. Case: toggles get a chip; a blank `;hello` passing.
- (2026-10-28) One action reached for two reasons gets copy true at each entry point. Case: rotate vs lost recovery key.
- (2026-10-31) Public claims (Pro features, supported sites) are re-checked against shipped features and the live-test record, not the older listing. Case: "folders" on the landing page; LinkedIn in the CWS listing.
- (2026-10-30) Onboarding copy names only what the onboarding creates, and copy after uninstall only actions possible without the extension. Case: ";hello"; "until you delete them".
- (2026-10-30) A page copying another project's model checks which styles and components the target site has. Case: side-by-side forms on a 720px site.
- (2026-11-04) Copy explaining an unbuilt feature uses the conditional in every line (title, steps, privacy claim) and says answers "help decide", never "decide"; a "considering" tag does not soften a present-tense title.
- (2026-11-04) Any listing or marketing line that repeats a product limit carries the same limit the UI shows (count and window). Case: "last 10 versions" in the CWS text, while the UI says "up to 10 versions … from the last 30 days".
- (2026-11-04) Store images and tiles get a `file` check for RGBA before every commit, no matter what an earlier commit message claims. Case: a commit said "no alpha", yet three of its files were RGBA.
- (2026-11-04) Before a public browser-store listing, review every platform the manifest declares, not only desktop. Case: `gecko_android`, added just to silence a lint warning, would have offered an untested Firefox for Android build.
- (2026-11-06) Reusing a component "as is" in a new context brings all its copy: list every string it can render (buttons, busy text, errors, sub-screens, the email it triggers) against the new context's banned words. Case: LinkFlow's "Link this browser" inside "Get Pro without linking".
- (2026-11-06) An action chained from a child's success callback never decides from props captured before the write; wait for the store change in an effect or decide from fresh state, above all when a wrong guess charges money. Case: auto-checkout for an already-Pro email, no server guard.
- (2026-11-06) When a flow's container unmounts on success, the plan names where focus lands and which status explains the new state. Case: the inline email/code flow vanishing when `linked` flips.
- (2026-11-06) Changing copy an e2e helper waits on means grepping the helpers too, not only the specs that name the flow. Case: `waitUnlinked` matching `billingLinkFirst` in ~18 call sites.
- (2026-11-06) A new permission changes what every state built on the old blind spot now sees: re-check each "no access here" branch and its copy, and classify pages that can never run scripts by an injection attempt, not by URL scheme or `permissions.contains`. Case: host permissions exposing tab.url moved the Chrome Web Store tab from "unknown" to "Reload this page".
- (2026-11-06) A lifecycle fix lists every way an extension restarts (install, update, re-enable, settings-triggered reloads, browser restart), not only the one reported. Case: `onInstalled` misses re-enable after a disable; a `storage.session` flag on worker start covers all.
- (2026-11-06) An orphaned-context test keeps the caret in the field across the update; any later focus makes the old script inert on its own, so "no error" passes without the fix.
- (2026-11-06) Adding a permission updates the architecture doc's "not requested" list, the manifest test's exact permission list and the store's per-permission justification fields in the same change.

## Moved from work-project critics (2026-11-06) — cross-project
- 2026-11-03: In strict structured output, declare a diagnostic field after the payload; properties are generated in schema order, so an earlier field steers the decision (`unsupportedReason` after `setup`).
- 2026-11-03: A reason enum must cover every refusal branch of the prompt and include `OTHER`, or the model forces the nearest wrong label (documented-but-unsupported auth vs undocumented auth).
- 2026-11-04: Test new classification logic through the outermost real mock (openai), not by mocking the function that contains it.
- 2026-11-04: Never map indexes from a `toLowerCase()` copy back to the original (`'İ'` changes length); use a case-insensitive RegExp with `lastIndex` on the original.
- 2026-11-04: A ReDoS fix must also time the per-match work (a line scan per link), not only the regexes; measure every stage with adversarial input.
- 2026-11-06: A repair loop that re-prompts with the execution error's diagnostic gives attempt 2 no knowledge of why attempt 1's repair was rejected; feed the rejection reason into the next diagnostic.
- 2026-11-06: "Stop on an empty page" is per-API; measure the over-range response per platform (Woo `[]`, Magento `items: []`, Pimcore 0 edges) before setting a request-count bar, and prefer a short-page stop.
- (2026-11-06) When a list drops its source's description line, each bare name must still be true on its own. Case: "Outlook" without "on the web" claims the desktop app.
- (2026-11-06) A "where it works" answer names the most likely place it doesn't work, next to the list. Case: Google Docs left only on Help.
- (2026-11-06) A test keeping two copied lists in sync compares them both ways, read only from the source's own container, never by substring. Case: `'X'` matches any capital X in Help.
- (2026-11-06) A navigation guard on `popstate` reverts by stack position (an index in `history.state`, `history.go(±delta)`, echo ignored), never by pushing the old address; typed or anchor hashes (state null) fall back to `replaceState`. Case: ghost Pricing entries from a pushState revert.
- (2026-11-06) When a history entry shows a different view than its hash, the address is rewritten with `replaceState`, or a reload and the Back menu contradict the screen. Case: `#welcome` mapped to the library after Skip setup.
- (2026-11-06) "As it does today" in a plan is checked in code (and scroll/focus after Back measured) before it becomes the spec. Case: "starts at the top as on a click" with no scrollTo anywhere; the browser restores 2000 px after Back.
- 2026-11-03: Keep a log out of a `try` that maps every error to one code, so a logging failure cannot surface as that code (`invokeModel.ts`).
- 2026-11-04: A limit test that asserts only text shared by every budget error passes for the wrong limit; assert the class or the specific reason.
- 2026-11-04: When a refusal is correctable only under a job condition, throw the reason from the model wrapper and decide in the caller that owns the job.
- 2026-11-05: A measurement that says "read X if reachable" must confirm the read path before the deploy; usage stored only in a deployed DB needs a log line.
- 2026-11-05: A model-setting comparison where the inputs also differ is not evidence; call the quality effect unknown and decide on cost and budget.
- 2026-11-05: Detect "our deadline fired" with `signal.aborted` where the signal lives, not by error name higher up; the same abort surfaces as TimeoutError, APIUserAbortError or AbortError, and converting it higher up loses state such as usage.
- 2026-11-06: `jest … | grep` hides the exit code; capture the output and fail on "failed" before a commit step runs.
- 2026-11-03: Adding an output field to a structured-output schema changes model behavior; never call such a change "diagnostic only, no behavior change".
- 2026-11-03: A defensive guard is "strong" only if the guarded state can occur; check the real trigger path first (workspace switch reloads the page).
- 2026-11-04: A self-repair fix is proven only by runs where the repair actually ran, counted over ≥3 runs against a baseline.
- 2026-11-05: Write the A/B success threshold before running; a refusal that only changes reason is no progress.
- 2026-11-05: At n=8 set the pass bar against the baseline, not another arm's point estimate (fails ~1/3 of the time on noise).
- 2026-11-05: Before fixing an intermittent fault inferred from timing gaps, add the log that shows it directly (elapsed time per model call).
- 2026-11-05: A failure counter kept in state must reset on every path that clears the error it guards (Retry, reopen), or the next attempt starts used up.
- 2026-11-09: Set a loop's deadline where its abort signal is created, not after an earlier await (`processJob` set it after `fetchDocumentation`).
- 2026-11-09: Raising a retry count exposes later attempts to every budget created once per run; a later "budget spent" probe must not overwrite earlier evidence.
- 2026-11-09: Before replacing a fallback error code, read the test and commit that introduced it; "refused repair → integrationSetupIncomplete" routed users to Instance details on purpose.
- 2026-11-09: A pass-bar input carries only what the user-facing copy asks the user to type; extra hints (parameter names) measure a path no user takes.
- 2026-11-09: When an error asks the user to type a value, check where they can see the valid values; if only the log has them, show them (Akeneo locale/channel codes).
- 2026-11-09: A sentence added to a shared prompt block changes that stage for every source; count it against every row measured at that stage.
- 2026-11-10: An out-of-repo prerequisite checklist for a new queue/service must cover the producer's permissions (e.g. SendMessage) as well as the consumer's config, and becomes a release condition written in the MR.

## From MarketClean, 2026-11-13 (critic-engineering)
- A DOM marker measured inside element X proves nothing for a function that receives an ancestor of X; scope the code to what was measured, or re-measure on the real argument.
- Widening a matcher shared by two predicates with different intents changes both; check each predicate's own exclusions first.

## From MarketClean, 2026-11-13 (repeat-trials report, both judges)
- A cron add-on that only sends on success turns a broken query into a silent week; its failure goes in the email it would have sent, not only the run record.
- Before reading a ledger as "what happened", list every path that deletes from it (a rolled-back claim records grants, not attempts).
- A "status" report on a fix shows whether the fix works (blocked attempts), not only that the problem exists.

## From lamp, 2026-11-13 (plan judges)
- macOS launchd agents can't read `~/Desktop`, `~/Documents`, `~/Downloads` (TCC); a manual Terminal run passes, so check the job's own log. Keep scheduled projects outside those folders.
- A look-ahead window must clamp at the end of its range; test the last slot.
- Messages queued in advance must not depend on state later runs can change; decide at send time.

## From MarketClean, 2026-11-13 (denied-installs fix, both judges)
- An event keyed per (doc, install) but storing only the install is looked up by its exact `_id`; a query on the install id mixes in other docs' events and can hide a real alert.
- Read what a timestamp field is set to before using it as "when it happened" (a link's issue time is not its click).
- A replay of a "last 24h" query at a past time must cap the window's end too, or every past day sees today's data.

## 2026-11-14 — offer widened to live trials (MarketClean Black Friday)
- Opening an offer to a new group means rereading every string that group sees ("Pro adds…" shown to people already on a Pro trial).
- A campaign started early to catch a group counts who fell just before the start, and decides on purpose whether they get a message.
- Widening an offer to live trials: check every "already paid?" test the trial emails use; email-only matching misses a restored browser that paid under another address.
- A server text or health detail that describes who gets a feature changes in the same commit as the gate.

## 2026-11-14 — page overlap fix + outreach/flip prep (MarketClean)
- A layout measurement renders the real i18n strings with real substitutions, never placeholder text.
- A positioning fix states its clearance as a formula (obstacle bottom + element height + offset) and tests real inner-viewport heights, not screen sizes.
- To find who got an email without an offer, filter on its sent-at field against the flip time and the cron's real schedule, not the deadline date.
- A script that builds a link with an env-driven parameter asserts the parameter is in the output; locally the env is unset.
- A decision built on replies to a small outreach sets its default from data already held; replies overturn it by content, not count.
- A feedback tally also flags the replies that need an answer; a bug report from a former user is support, not a data point.
- A rule that overrides max-width keeps the original cap via min(origCap, newLimit); bounds for a content-box element include its padding.
- A nowrap box under a max-width clamps the box, not the text: assert scrollWidth <= clientWidth, not only the rect.
- An overlay audit lists every fixed-position element the stylesheet defines and every caller of the shared notice factory, not the ones in the bug report.
- A "fails before the fix" test claim names the exact size and locale the measurement showed failing.

## 2026-11-14 — daily alerts → weekly report + urgent-only (MarketClean)
- Whether an alert interrupts the owner depends on what it puts at risk, not on its severity label.
- Mark an alert delivered only after the send succeeds; otherwise the "email is failing" alert can never get through.
- A weekly digest that replaces daily alerts lists what was flagged and cleared during the week.
- An alert keyed on "new since the last run" traces how a failing group renames its checks.
- A field added to a run record is missing from every older record; the plan says what the first run does.

## 2026-11-14 — Fable ops agent (MarketClean)
- When a report becomes the only signal, its silence is detected by something other than the reader; a dead-man records the end of the job, not its first read.
- An agent's standing context has an expiry date per item and an owner who updates it; assistant-owned upkeep goes in the weekly digest, never an email.
- Before automating a judgment someone liked, check every fact behind it is in the data the automation reads; porting a scratchpad census re-derives hard-coded constants from stored fields.
- Before exposing check output to a new reader, grep every detail for raw identifiers.
- A job scheduled after a Vercel Hobby cron leaves the one-hour late-start window.
- A reminder needs a "done" signal from the data; walk new alert rules day by day against the real calendar before shipping.
- A daily cap guarding a send fails closed (reserve before, release on failure), never a counter that returns null on a DB error.

## 2026-11-15 — store listings price disclosure (MarketClean)
- A price block needs a Free/Pro mark on every feature heading below it; one block doesn't relabel the sections.
- A privacy line written before a product took emails is re-checked whenever the copy starts inviting sign-ups.
- A per-store copy fix starts by grepping every claim on the topic in each store; a new disclosure deletes the older sentence making the same claim.
- Store copy lists features from the public list (landing FAQ), not rebuilt from the code gates.
- "Draft" means something different in each store: read every dashboard's status before editing.
