---
name: standard-review
description: Review a feature's changed files for code shape — shared types living in the right place, no oversized multi-responsibility files (extract helpers, co-locate a component with its styles in its own folder), clear folder structure, and no ambiguous naming. Applies the warranted, behavior-preserving refactors on the current changelist and flags judgment calls. Never changes runtime behavior. Use when asked to do a standard review, review code quality/structure, check shared types, split big files, or tidy the folder structure of a feature/branch/changeset.
---

You review and improve the STRUCTURE and CLARITY of the code a feature added or changed. You make behavior-preserving edits only — never alter runtime logic, control flow, or output.

## Scope

- Target the ENTIRE current feature by default: every file changed on this branch versus the branch it merges into, plus any uncommitted changes. Build the file set from `git diff --name-only <base>...HEAD` (base = the target/default branch — try `origin/master`, `master`, `origin/main`, `main`, then `stage`) plus `git status --porcelain` (uncommitted, incl. new files).
- If the user names specific files, paths, or a branch/base, scope to those instead.
- Only review code the feature added or touched — do not restructure the whole pre-existing codebase.
- Read the repo's `CLAUDE.md` (root and any nested one for the touched directory) FIRST and treat its conventions as binding; they override the generic guidance here on conflict.

## What to check (the four axes)

1. **Shared types in the right home.** A type used by more than one file must live in the module's shared types file (e.g. `types/`), not buried in a hook, component, or the file that happened to define it first. Flag duplicated type shapes and re-home cross-file types. Do NOT create pass-through re-exports or trivial aliases (`export type A = B`) — move the definition and update importers to the canonical path.
2. **No oversized, multi-responsibility files.** A file doing two distinct jobs (e.g. inline parsing + block parsing, transport + state, fetch + transform) should be split into focused helper files. Prefer small, single-purpose modules over one long file. Judge by responsibility count and readability, not a hard line limit — a cohesive class or state machine may be long and should stay whole; don't split when splitting hurts cohesion.
3. **Clear folder structure.** Co-locate a UI component with its styles in its own folder (`Component/Component.tsx` + `Component/Component.styles.ts`), and put a helper next to what it serves. Keep the dependency direction sane (a `utils/` helper should not reach into `components/` styles — move it where it belongs). Mirror the structure the module/repo already uses.
4. **No ambiguous code.** Rename vague identifiers (`data`, `info`, `payload`, `temp`, single letters outside tight loops) to the real domain word; remove unexplained abbreviations; make references unambiguous. Match the project's own naming patterns (check sibling files). Clarity of names beats a comment explaining a bad name.

## Process

1. Build the file set (Scope) and read the changed files plus the closest sibling files, so refactors match existing patterns.
2. For each axis, list concrete findings with `file:line`, each labelled **apply** (clear win) or **flag** (judgment call for the user).
3. Apply the **apply** findings — behavior-preserving only. Update every importer when you move a type/file. Keep edits minimal and idiomatic to the surrounding code.
4. Leave **flag** items unedited and report them with a one-line recommendation for the user to decide.
5. Verify: run the project type check, linter, and build if available; confirm they pass and that no runtime behavior changed (diff should be moves/renames/splits, not logic edits). For UI moves, a quick smoke check (build + render) is worth it.
6. Report: a short list of what you applied (grouped by axis) and what you flagged, each with its reason.

## Stop conditions — do not cross without asking

- Do NOT change runtime logic, behavior, control flow, or output — structure and names only.
- Do NOT restructure files outside the feature's changed set.
- Do NOT introduce new dependencies, abstractions for hypothetical future use, or broad renames across untouched code.
- Do NOT add pass-through re-exports or trivial type aliases to avoid updating importers — update the importers.
- Do NOT reformat or restyle untouched lines; keep the diff logic-free and scoped to the review.
- Do NOT `git commit` or `git push` unless explicitly told to.
- If a structural fix would require a behavior change, stop and flag it instead of doing it.
