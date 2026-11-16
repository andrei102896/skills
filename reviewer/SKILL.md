---
name: reviewer
description: Review your own branch or a GitHub pull request in a personal or solo repository, any stack. Hunts correctness bugs in the changed logic first (callers of changed contracts, readers of changed data), then checks how the task was shipped — root cause at the shared choke point, every sibling and consumer updated, bounded and resilient IO, named tunables, docs and description in step with the code — plus the built-in review rules and the project's own `.claude/review-rules/`. A walkthrough index orders the diff by call, diffs over 30 files are split into zones, one agent per rule group judges in parallel, and a fresh agent verifies every finding. Findings carry evidence, never the fix, in a findings file grouped as proven fix / one question / your call / escalation; then walks the author through each one (fix / not now / not valid / re-check), resumes where it stopped, and learns from rejections. Read-only except accepted fixes; never posts comments anywhere. Use for "/reviewer", "/reviewer <PR number or branch>", "/reviewer quick", "/reviewer --learn".
argument-hint: "[<pr#|branch>] [--base <branch>] [--uncommitted] [--fix-a] [--worktree] | quick [--base <branch>] | --learn [branch]"
---

# Reviewer

Review the target in `$ARGUMENTS` the way a careful senior engineer reads a change before it ships: first "what
breaks?", then "is this the root cause or one symptom site?", "where else does this live?", "what bounds it, times it
out, cleans it up?", "where did this number come from?" and "do the description, docs and tests tell the same story as
the code?". Every finding carries its proof from code or usage, never the fix: the author knows the code and picks it.

`<skill dir>` below is the base directory Claude Code shows when this skill loads. Scripts run as
`python3 -B <skill dir>/scripts/<name>.py` from the repository being reviewed.

## Never

- Edit code, except fixes the author accepts in triage and `--fix-a`.
- Check out, switch, pull, stash, reset, commit or push in the user's working copy.
- Post, comment, approve or reply on the pull request or anywhere else.
- Print tokens or secrets. Write findings in any language but English.
- Launch an agent as a fork, or on any model other than `model: "opus"` with `effort: "medium"`.

The project's `CLAUDE.md` / `AGENTS.md` win over this skill on any conflict.

## 0. Mode — pick exactly one

Read `$ARGUMENTS` in this order: the sub-command words `quick` and `--learn` first, then the flags, and only then a
remaining word as a PR number (`12`, `#12`, or a PR URL → its number) or a branch name.

| Invocation | Do |
|---|---|
| `/reviewer` | author mode on the current branch: the full flow below, then triage |
| `/reviewer --base <branch>` | author mode against that base instead of the guessed one |
| `/reviewer --uncommitted` | author mode including staged, unstaged and untracked edits (a snapshot, nothing touched) |
| `/reviewer <pr#\|branch>` | PR mode: the full flow on that PR; ends with the findings file, no triage |
| `/reviewer <pr#\|branch> --worktree` | [worktree.md](references/worktree.md) first, then PR mode inside the worktree |
| `/reviewer <pr#\|branch> --fix-a` | PR mode, then apply the section A findings the verifier kept (see 7) |
| `/reviewer quick [--base <branch>]` | [quick.md](references/quick.md) only |
| `/reviewer --learn [branch]` | [learn.md](references/learn.md) only; no review |

`--uncommitted` and `--base` belong to author mode; `--worktree` and `--fix-a` to PR mode; `--worktree` and
`--fix-a` never combine with `quick` or `--learn`. An unknown flag → say so and stop.

## Flow — prep → scope → gather → judge → write → verify → close → triage

Do not start a phase before the previous gate passes. Keep the main thread small: it reads prep's output, the
walkthrough index and the agents' answers, never the code. Batch independent calls in one message.

### 1. Prep

Run `python3 -B <skill dir>/scripts/prep.py [<pr#|branch>] [--base <branch>] [--uncommitted]` (no argument = author
mode). Act on its lines:

- `STOP: <reason>` → explain the reason in one line and stop. When the reason is that the checkout is not the PR head,
  offer `--worktree`. When `gh` is missing or no PR matches, ask which PR or suggest checking the branch out and running
  `/reviewer`.
- `UNCOMMITTED <n>: <paths>` → one AskUserQuestion, header `Uncommitted`: "Review them too" → rerun prep with
  `--uncommitted` and continue from its output; "Stop and commit" → stop. Never commit or stash for them.
- `RESUME <file>: <ids>` → skip phases 2–7. Say "continuing <file>, <n> left" and go to 8 with those ids. Edits already
  in the tree are the fixes made so far: never stash or question them.
- Otherwise keep: `base: <ref> (<how>)` (say the base, and that it was guessed when it was), `range:`, `files:`,
  `ZONES REQUIRED`, `walkthrough:`, `findings file: <path> (r<N>)`, the `prior findings:` block, and in PR mode
  `pr:`, the `pr comments:` block and any `stacked:` lines.

Gate: no `STOP:`, no unanswered `UNCOMMITTED`.

### 2. Scope

- `ZONES REQUIRED` → [zones.md](references/zones.md). Do not continue until the user picked the zones.
- Otherwise the whole diff, one pass, no question.

### 3. Gather

[gather.md](references/gather.md): run the `walkthrough:` command (plus one `--zone` per picked zone), read the index,
keep its `## Groups` table. Gate: the index file exists and its `## Groups` table is read.

### 4. Judge

[groups.md](references/groups.md): one agent per group row whose hunks are not `none — skip`, plus the delivery agent,
all in one message. Wait for every answer, then merge. Gate: every launched agent answered or is named as failed.

### 5. Write

Write the findings file at prep's path in the shape of [format.md](references/format.md), applying
[evidence.md](references/evidence.md) to every merged finding. A candidate that fails its evidence row is dropped here.

### 6. Verify

[verify.md](references/verify.md): one fresh agent per changed file with findings, all in one message; record the
verdicts in the file. Gate: every file with findings has a verdict per finding.

### 7. Close

1. Append the usage section: `python3 -B <skill dir>/scripts/usage.py <session-id> >> <findings file>`. The session id
   is the directory just before `/scratchpad` in the scratchpad path from your system prompt. In a worktree, run it
   from the main checkout.
2. `--fix-a` only: apply every section A finding whose box reads `request change — **verify:** holds`, append
   ` — **author:** fixed` to that line, then run the project's lint and focused tests on the changed files. In a
   worktree the edits land in the worktree: say so.
3. Print to the terminal: one verdict line (`ship` / `ship after fixes` / `rework` — one line why), counts per section,
   the ids verify found `doubtful` or `wrong`, the findings file path, agents that failed, and zones not reviewed yet.
4. PR mode ends here: "tick the boxes in the file, or check out <branch> and run `/reviewer` to triage — it resumes
   this file". Author mode continues with 8.

### 8. Triage (author mode, and RESUME)

[author-mode.md](references/author-mode.md): every answer is written into the file at once; fixes are applied only
after the author picks them. End with the summary line, the files changed and "review the diff, commit, push".

## Principles every phase applies

- **Correctness first.** Hunt what breaks before any convention; a reviewer that only applies rules misses the bugs.
- **Proof from the code, not opinion.** Every finding has an `Evidence:` line: the only caller, the reference count,
  the line that overwrites, the constant that bounds it. Count uses before calling anything too complex or unused.
- **Never the fix.** What is wrong, what it causes and how you know. Naming the existing helper in a reuse finding is
  evidence, not a fix. No `Fix:` lines, replacement code or "consider…".
- **Group by what validating costs the author.** A = proven, confirmed in seconds; B = one question decides it, with
  what each answer means; C = a tradeoff in one line; D = structural: name what is wrong and where the decision
  belongs, never invent the redesign.
- **Ask instead of assuming across a boundary.** A fact in another service or repo is a B question.
- **Scale from the codebase's own numbers.** Quote the constant or limit that sizes the risk, not a guess.
- **Conventions are not demands.** Where the codebase is split between two patterns, name the split and its motive.
- **Split a finding with two halves** (the A part and the C part) into two findings.
- **Hold the code to its spec.** A feature spec, README or progress doc is checked claim by claim against the code.
- **Rounds.** A finding answered **not valid** earlier is never raised again, even on new code; **not now** returns only
  if the new code makes it worse; **request change** still present is carried over and named in the header.

## Lens — the correctness and delivery agents' checklist

The correctness agent owns 0, 2, 3, 5, 6, 7 and 8; the delivery agent owns 1, 4, 9, 10 and 11. Rule-group agents use
their rules instead.

### 0. Correctness
- For each changed function or handler, trace what can reach it: null, empty and missing values, the boundaries of
  every condition and index, each `await` and its error path (thrown, swallowed, not awaited), a state update racing
  another, cleanup on unmount or failure, a cache or map that only grows. A failure you can name is a **Bug**: the
  input or sequence, and the wrong result.
- A changed pure function (parser, formatter, regex, encoder, validator, arithmetic) is run with edge inputs in a
  throwaway script: "reproduced: input X → output Y". A regex over untrusted input gets a timing run on a long
  adversarial string.
- Callers of changed contracts and readers of changed data: the two procedures in [gather.md](references/gather.md).

### 1. Root cause at the choke point
- The fix lives where all callers route through (shared helper, resolver, provider, lookup, reducer), not as a guard in
  the one caller that crashed. N per-consumer guards for one cause is a finding.
- Every sibling changes in the same diff: copy-pasted helpers in parallel folders, every package consuming a bumped
  dependency, every entry point that used the replaced code, every registry (types, enums, schemas, constants,
  defaults). A data-contract change reaches every consumer: schema versions, converters, renderers, copy/export paths,
  readers in other languages. A data fix repairs existing records, not only new ones.
- Code deleted as "dead" comes with proof (grep plus stored or runtime sources). Side discoveries are tracked
  separately, not silently fixed inline or ignored.

### 2. Resilience at IO boundaries
- New network or SDK clients set a timeout, keep-alive when reused and a bounded retry; one client is reused, never
  created per call. Retries only on errors that can succeed. Queue consumers: visibility timeout above handler
  timeout, a dead-letter path.
- Resources (documents, pages, streams, temp dirs, handles) are released in `finally`; variables used in
  `catch`/`finally` are initialized before `try`. Cleanup that throws must not replace the original error or skip
  reporting the job as failed.
- A non-critical side pipeline (tracking, analytics) catches and logs its own failure and cannot break the main flow.
- Lookups fail fast with a named error instead of an `undefined` that crashes far away; a branch that records an error
  also returns. Promises started in init code are awaited or caught; a refactor must not drop a former `.catch`.
- Vacuous truths: `every` over an empty set, 0/0 counters, updates at index `-1`.
- Multi-write sequences: walk every failure point between the writes and say what is lost or doubled and whether
  anything retries it. Suggest a transaction only after confirming every write uses the same connection and database.
- A comment describing failure handling must hold for every failure path.

### 3. Bounded work and performance
- Batches, `IN (...)` lists and fan-outs are chunked by a named constant; concurrency is capped and sized to the real
  input. No-op work is skipped. Memory-bound inputs run sequentially. Blocking work stays off the event loop.
- Queries fetch only the fields they use and hit an index. Payloads crossing a size-limited boundary are measured
  against the limit for the largest real input. No `find` inside a loop over the same collection.
- Performance claims in the description come with measured numbers.

### 4. Tunables with provenance, one source of truth
- Timeouts, limits, thresholds, delays and sizes are named constants with the unit, reusing a shared one when it
  exists. Operational limits are overridable with a default and validated where read.
- A value mirrored in another file, language or service carries a "must match X in Y" pointer; a formula lives in one
  module. New config keys reach every environment. Infra limits change in deploy config, not around it in code.

### 5. Types and boundary validation
- Return types are as narrow as their consumers use them. Known shapes get explicit types; variants get discriminated
  unions. No new `any`, double casts or object-literal casts without a one-line reason.
- Real booleans and numbers cross boundaries (`'false'` is truthy). Unexpected data is an error, not a silent default.
  Untrusted stored data is parsed defensively. A "lint fix" must not change semantics.

### 6. Security
- No committed secrets. Credentials hashed at rest, consumed atomically, compared in constant time, kept out of token
  payloads. Signed URLs and tokens redacted before logging. Personal data stays out of URLs.
- User-controlled values reaching HTML, SVG, CSS or URLs are sanitized, with a test for the injection case. URL and
  domain checks parse and anchor the host. Resources are fetched through ownership-checking access, not by bare id;
  permissions are scoped. An automation acting for a user asks before outward actions.

### 7. Observability
- Log level matches meaning (failures at error), logs are structured and carry the entity id, and log text follows
  the algorithm when it changes. No `catch` that swallows without a log; no leftover debug output or flags.

### 8. Frontend (skip when the diff has none)
- Effects that add listeners, timers, frames or fetches clean up and guard against updates after unmount; deps are
  complete. A shared-layer fix beats per-component guards. A loading counter reaches "loaded" on every path; every
  loader has a failure state. JS binds to behaviour hooks, not styling classes; CSS is scoped, no `!important` patches.
- Accessibility: real buttons, `aria-expanded` in sync, Escape closes and restores focus, visible focus, touch targets.
- User-visible copy goes through translation keys in every locale. E2E tests wait on signals, never fixed sleeps.

### 9. Dependencies and migrations
- A shared dependency bump lands in every consuming package at the same version; lockfiles regenerated. Major
  upgrades carry their build and call-site work. Removing an unused package or using a built-in beats bumping it.
- Migrations ship ahead of the code that needs them, run online where the engine supports it, and have a working down.

### 10. Delivery — description, commits, docs, tests
- The PR description and main commit body are one causal chain: "<what broke>, because <mechanism>; now <fix>", with
  numbers when something was measured. One concern per change; unrelated edits split out or isolated in a disclosed
  commit. Commit subjects are specific and unique; no unfilled template placeholders.
- `AGENTS.md`, README, ADRs and specs change with the code when a command, algorithm, limit or convention changed, and
  every number, file and test they name exists and matches.
- The test plan is real for behaviour changes; regression tests pin the incident input; security-sensitive logic has
  tests. No scratch artifacts committed. Comments explain the non-obvious why and stay true.

### 11. Minimal surface, proved by usage
- A parameter no caller passes, a one-use wrapper, a forwarding helper; a construct chosen only to dodge a lint rule;
  the same constant, formula or status list in two places holding one domain rule (search for a third copy first; not
  a finding when sharing would need a helper with a mode because the consumers differ).

## Blind spots — check these hardest

Where shipped changes slip:
- unrelated changes bundled in; reformatting of untouched lines
- "test plan: n/a" on behaviour changes; no tests for new security logic
- vague or repeated commit subjects; placeholders left in commit bodies
- docs contradicting the code in the same change (stale limits, tests that do not exist)
- catches that swallow errors; effects without cleanup; no `return` after recording an error
- committed private keys; over-broad permissions
- small helpers copy-pasted across files instead of shared
- long speculative comments ("possible bug, unverified") instead of a fix or a tracked task

Where reviews slip:
- suggesting a transaction across writes that live in different databases or connections
- stopping the sibling search at two copies when a third exists
- pointing at code a lint rule covers without saying the rule applies
- computing a line number from a hunk header instead of reading the line
