# Templates

Placeholders: `{{NAME}}`, `{{PURPOSE}}`, `{{STACK}}`, `{{HOST_SITE}}`, `{{COMMANDS}}`, `{{DATE}}`, `{{REPO}}`.
Include "Extension discipline" only for browser-extension projects and "New package" only for the Node layout.

---

## AGENTS.md

```markdown
# AGENTS.md — {{NAME}}

Read before coding, in order: this file → README.md → PROGRESS.md → docs/ROADMAP.md.

## What this is
{{PURPOSE}}. Stack: {{STACK}}.

## Hard rules
- Max 300 lines per non-test file (ESLint `max-lines` enforces it); new files target ≤200. Check line counts of files you will touch; split an over-cap file before adding to it.
- Comments: max 2 lines, prefer 1, only the non-obvious "why". Never narrate changes. Re-read every comment before finishing.
- Types are defined, never asserted: no `as` (except `as const`), no non-null `!`, no `any`. External data is parsed with zod; types are inferred from the schema, not written twice.
- No barrel files. Import from the defining module.
- Pure logic separated from IO (network, DB, DOM, model calls); the pure parts get unit tests.
- One concern per change. No adjacent refactors, no scope expansion. No dead code, no commented-out blocks, no `console.log`.
- Shared values (thresholds, limits, prices) are named constants in the module that owns them.
- Every fix ships with its test. Never weaken a test to make it pass.

## Workflow
- A change that warrants a plan: plan → two judges (`critic-engineering`, `critic-design`) in parallel → revised plan with a findings table → Andrei's go → implement → tests → DoD → `/reviewer`.
- Accepted "Proposed lessons" go to `.claude/critics/<kind>-lessons.md` (created on the first one), dated, ~40 entries max.
- Measure the whole set before planning a fix; one sample is not a rate.

## Git
- Never push or deploy: Andrei does. Hand over the exact commands. Commit only when asked. No AI-attribution trailers.
- Commit email: purcar.andrei28@gmail.com (resolved from the `{{REPO}}` remote). Never a work identity.

## Definition of done
{{COMMANDS}}
All green before declaring done. List every file touched.

## New package (Node layout)
`packages/<name>/package.json`: `"name": "@{{NAME}}/<name>"`, `"private": true`, `"type": "module"`, `"exports": { "./*": "./src/*.ts" }`, `"scripts": { "typecheck": "tsc -p ." }`.
`packages/<name>/tsconfig.json`: `{ "extends": "../../tsconfig.base.json", "include": ["src"] }` (add `"lib": ["ES2024", "DOM"]` only where the package touches the DOM). Tests sit next to the code as `*.test.ts` (`node:test`). Create the package with its first real module and test, never empty: `tsc` fails on an empty `src`.

## Extension discipline (host: {{HOST_SITE}})
- Never depend on the host's obfuscated class names — anchor to text/structure/`role`/`data-*`/href patterns with confidence scoring (soft signals, no hard gates).
- Read-only toward the host: never automate clicks/requests, never restructure its DOM, clear injected markers on recycle/disable.
- Single evaluation pipeline for initial + dynamically-added items; one MutationObserver on the root, batched per animation frame; never polling.
- Per-item fault isolation (try/catch, count, continue). Detection failure → log and skip.
- Duplicate-injection guard in every entry point; error handling within a few lines of every async platform call.
- Least-privilege permissions, each justified in README. Minimal egress by explicit allowlist.

## Docs upkeep
- Docs are the source of truth: update them in the same change or stop and ask.
- Record regression guards (incident + "do not remove") and dead ends (evidence + "do not rebuild") in README.md.
- Log decisions in PROGRESS.md, dated. Tick tasks in docs/ROADMAP.md in the change that completes them.
```

---

## README.md

```markdown
# {{NAME}}

{{PURPOSE}}

## Stack
{{STACK}}

## Run / validate
{{COMMANDS}}

## Architecture map
<!-- One line per file/folder. Keep current — this is how an agent knows where new code belongs. -->

## Permissions & egress (extension projects)
<!-- Each manifest permission with its justification; exact allowlisted payloads that may leave the machine. -->

## Regression guards
<!-- Behavior + incident that caused it + "do not remove this guard". -->

## Dead ends
<!-- What was tried, what was measured, why removed. Do not rebuild without new evidence. -->
```

---

## PROGRESS.md

```markdown
# PROGRESS — {{NAME}}

Decision log. Dated entries, newest first. Prune completed work; history lives in git.

## Deferred decisions

## Rejected decisions

## Open questions
```

---

## docs/ROADMAP.md

```markdown
# Roadmap — {{NAME}}

The tracker. Tick a task in the change that completes it; dated.

## Now

## Next

## Later
```
