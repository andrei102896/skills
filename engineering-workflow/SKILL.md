---
name: engineering-workflow
description: Apply a project-aware software-engineering workflow for substantive implementation, bug fixing, refactoring, debugging, configuration, testing, code review, and codebase investigation. Use automatically when work requires repository discovery, code changes, validation, or an evidence-backed technical assessment. Do not trigger for casual conversation or simple factual questions unrelated to a project.
---

# Engineering Workflow

Apply the workflow silently. Do not require a slash command or ask the user to choose a workflow.

## Classify intent

- For explanation, review, audit, or diagnosis, inspect and report without editing unless the user requests a fix.
- For implementation, fixing, refactoring, migration, or configuration, complete and verify the requested change.
- Treat commit, push, deploy, publish, deletion, reset, and external messaging as separate actions requiring explicit authorization.

## Discover the project

1. Determine the working and project roots.
2. Inspect version-control status before editing.
3. Read applicable instruction files, including `AGENTS.md`, `CLAUDE.md`, nested guidance, `.claude/rules/`, specifications, and development documentation.
4. Identify the language, package manager, build system, and supported validation commands.
5. Preserve unrelated and uncommitted user changes.

Avoid repeatedly loading unchanged context.

## Execute

1. Establish concrete success criteria from the request.
2. Inspect relevant code paths before editing.
3. Make reasonable low-risk assumptions; ask only when a missing choice materially changes the outcome or safety.
4. Use a short plan only for genuinely multi-step work.
5. Implement the smallest complete solution consistent with existing architecture.
6. Avoid speculative abstractions, unrelated cleanup, and broad dependency changes.
7. Add or update focused tests when appropriate.
8. Run the narrowest relevant validation first, then broader project checks when justified.
9. Fix failures caused by the change and distinguish unrelated pre-existing failures.
10. Review the final diff for correctness, regressions, accidental edits, and missing tests.

Delegate only independent research, review, or noisy test/log analysis when isolation materially saves time or context. Keep small or tightly coupled work in the main thread.

## Finish

Lead with the outcome. Report important files, validation evidence, and unresolved risks or blockers. Do not claim success without evidence.
