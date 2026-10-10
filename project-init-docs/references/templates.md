# Templates

Placeholders: `{{NAME}}`, `{{PURPOSE}}`, `{{STACK}}`, `{{HOST_SITE}}`, `{{COMMANDS}}`, `{{DATE}}`.
Include the "Extension discipline" AGENTS.md section only for browser-extension projects.

---

## AGENTS.md

```markdown
# AGENTS.md — {{NAME}}

Read before coding, in order: this file → README.md → PROGRESS.md.

## What this is
{{PURPOSE}}. Stack: {{STACK}}.

## Hard rules
- Max 300 lines per non-test file; new files target ≤200. Preflight line counts on files you will touch; if one is over cap, split it first.
- Comments: max 2 lines, prefer 1. Only the non-obvious "why". Never narrate changes. Re-read every comment before finishing.
- TypeScript strict; no `any` without `// @agent-allowed: any because …`; `unknown`-first parsing of external data.
- One concern per change. No adjacent refactors. No scope expansion.
- No dead code, no commented-out blocks, no `console.log` in committed code.
- Shared values live in constants modules — no magic strings across boundaries.
- Pure logic separated from side-effect/DOM/IO code; pure halves get the unit tests.
- No barrel files. Import from the defining module.
- Every feature/fix ships with its test. Never weaken a release-blocking test — park as `test.fixme` with evidence.

## Git & releases
- NEVER run git commands or deploy/publish. Leave working-tree changes and hand over exact commands. No AI-attribution trailers.

## Definition of done
{{COMMANDS}}
All green before declaring done. List every file touched.

## Extension discipline (host: {{HOST_SITE}})
- Never depend on the host's obfuscated class names — anchor to text/structure/`role`/`data-*`/href patterns with confidence scoring (soft signals, no hard gates).
- Read-only toward the host: never automate clicks/requests, never restructure its DOM, clear injected markers on recycle/disable.
- Single evaluation pipeline for initial + dynamically-added items; one MutationObserver on the root, batched per animation frame; never polling.
- Per-item fault isolation (try/catch, count, continue). Detection failure → log and skip.
- Duplicate-injection guard in every entry point; error handling within a few lines of every async platform call.
- Least-privilege permissions, each justified in README. Minimal egress by explicit allowlist.

## Docs upkeep
- Docs are source of truth — update in the same change or stop and ask.
- Record regression guards (incident + "do not remove") and dead ends (evidence + "do not rebuild") in README.md.
- Log deferred/rejected decisions in PROGRESS.md, dated.
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
