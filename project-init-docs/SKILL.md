---
name: project-init-docs
description: Generate the initial md files for a new project — AGENTS.md, README.md, PROGRESS.md — seeded with Andrei's consolidated engineering rules (from market-clean, nn-chrome-extension, tomapan). Use when starting a new project/repo or when asked to "init project docs", "create AGENTS.md", or "set up project rules".
---

# project-init-docs

Generate `AGENTS.md`, `README.md`, and `PROGRESS.md` for a project, seeded with the consolidated rule set in `references/common-rules.md` and the skeletons in `references/templates.md`.

## Workflow

1. **Determine project identity** — infer as much as possible from the repo before asking:
   - Project name, one-line purpose, current stack (language, framework, package manager, test runner).
   - Is it a **browser extension**? If yes: which host site(s) does it run on, and manifest version.
   - Validation commands that exist (`typecheck`, `lint`, `test` scripts).
   Ask the user only for what cannot be inferred (typically: purpose and host site for a brand-new empty repo).

2. **Generate the three files** from `references/templates.md`, filling placeholders:
   - `AGENTS.md` — short, imperative session bootstrap: read order, hard rules, off-limits zones, DoD commands. Include the **extension-discipline section only if the project is a browser extension**.
   - `README.md` — product summary, stack, how to run/test, architecture map (one line per file/folder as the project grows).
   - `PROGRESS.md` — decision log with `## Deferred decisions`, `## Rejected decisions` (with reason), `## Open questions`, all entries dated.

3. **Never overwrite an existing file without confirmation.** If any of the three exists, show a diff-level summary of what would change and ask first.

4. Rules come from `references/common-rules.md`. Copy the rules relevant to the project's stack into AGENTS.md (don't link to the skill from the repo — the repo must be self-contained). Where two source rules differ, the stricter one is already the one recorded.

## Notes

- The rule set is the union of three real projects (market-clean, nn-chrome-extension, tomapan), strictest-wins. Update `references/common-rules.md` when a new durable rule is learned in any project.
- Keep AGENTS.md under ~120 lines: it is a bootstrap, not an encyclopedia. Long-form standards belong in README.md sections.
