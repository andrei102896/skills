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
- Never mention Flipsnack or use a work identity; public contact `andrei.projects@proton.me` (MC, DL, MIA; founder decision 2026-10-22).
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
