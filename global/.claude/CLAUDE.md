# Global engineering agreements

## Intent

- Answer, explain, review, audit, or diagnose by inspecting and reporting; remain read-only unless implementation is requested.
- Build, implement, fix, refactor, migrate, or update by completing and validating the requested change.
- Commit, push, deploy, publish, delete, reset, or message external systems only when explicitly requested.
- Classify intent silently; do not require the user to select a workflow.

## Project discovery

At the start of meaningful work:

1. Determine the working and project roots.
2. Inspect version-control status when available.
3. Read applicable project guidance such as `AGENTS.md`, `CLAUDE.md`, nested instruction files, `.claude/rules/`, specifications, READMEs, and development docs.
4. Follow more specific project guidance over these personal defaults.
5. Identify the language, package manager, build system, and supported validation commands.
6. Preserve unrelated and uncommitted user changes.

Do not repeatedly load unchanged context.

## Execution

- Prefer efficient search tools such as `rg` and `rg --files` when available.
- Inspect relevant code before editing.
- Make reasonable low-risk assumptions and continue.
- Ask only when a missing choice materially changes the result or creates meaningful risk.
- Use a short plan only for genuinely multi-step work.
- Implement the smallest complete solution consistent with existing architecture.
- Avoid speculative abstractions, unrelated cleanup, and unnecessary dependency changes.
- Add or update focused tests when appropriate.
- Run narrow validation before expensive repository-wide checks.
- Distinguish failures caused by the change from unrelated pre-existing failures.
- Verify outcomes and review the final diff before claiming success.
- Delegate only independent work when isolation materially improves speed or context use.

## Plans get two judges

- Any task that warrants a written plan (multi-file, risky, new feature or project, also releases and outreach) gets two judges before execution; in plan mode, before ExitPlanMode. One-line and copy-only changes get none.
- Judges are fresh agents, never forks: the project's `.claude/agents/critic-engineering` and `critic-design` if present, else the user-level pair. Each gets the plan and the user's request verbatim; both run in parallel, one round, again only if the scope changes.
- Hand over the revised plan with a findings table (adopted, or rejected with the reason and the judge's words), then wait for the go.
- Append accepted "Proposed lessons" to the project's `.claude/critics/<kind>-lessons.md` (create it on the first one), dated; keep each under ~40 entries and move cross-project ones to `~/.claude/skills/project-init/references/common-rules.md`.

## Communication

- Lead with outcomes and keep progress updates concise.
- Do not narrate every trivial command.
- Finish with what changed or was discovered, important files, validation evidence, and unresolved risks or blockers.
