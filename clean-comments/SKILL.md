---
name: clean-comments
description: Clean the comments across an entire feature's changed files — rewrite each to be unambiguous, at most two lines, and explain why (not what), and delete redundant ones that restate code, narrate a change, or record task/feature history. Comment-only; never changes code behavior. Use when asked to clean up, tidy, rewrite, or trim comments for a feature/branch/changeset.
---

You rewrite and prune code comments. You change comments only — never the code's logic, behavior, or formatting of code lines.

## Scope

- Target the ENTIRE current feature by default: every file changed on this branch versus the branch it merges into, plus any uncommitted changes — not a single file. Build the file set from `git diff --name-only <base>...HEAD` (base = the target/default branch — try `origin/main`, `main`, `master`, then `stage`) plus `git diff --name-only HEAD`.
- If the user names specific files, paths, or a branch/base, scope to those instead.
- Clean the comments the feature added or touched — do not rewrite the whole codebase's pre-existing comments.
- Comment-only edits. If a comment edit would require touching a code line, stop and flag it instead.

## Rules for every comment

1. **Max two lines.** If it needs more, the comment is doing the code's job — shorten it or delete it.
2. **Unambiguous.** No vague pronouns ("it", "this") without a clear referent; name the thing.
3. **Explain WHY, not WHAT.** The code already says what it does. A comment earns its place only by giving the non-obvious reason, constraint, or gotcha.
4. **Delete redundant comments** — ones that restate the code, state the obvious, narrate the change you just made, or record task/ticket/feature history. Prefer a clearer name or clearer code over a comment.
5. **Keep genuinely useful comments.** Non-obvious invariants, race conditions, workarounds, "why not the simpler way" — trim to ≤2 lines, don't remove.
6. **Don't invent explanations.** Only write a reason you can verify from the code or the user; if you don't know why, don't fabricate a why — leave the existing comment or ask.
7. **Match the language's comment syntax**, and respect project rules about where comments break tooling (check for a CLAUDE.md / repo convention first — e.g. some setups forbid comments in certain files).

## Process

1. Read the target and list its comments (and the code each annotates).
2. For each: keep-as-is / rewrite (unambiguous, ≤2 lines, why-focused) / delete (redundant).
3. Apply the edits. Leave pre-existing meaningful comments alone unless clearly redundant.
4. Verify the result: run the project linter/formatter if available and confirm **no code line changed** (e.g. `git diff` shows comment-only hunks).

## Stop conditions — do not cross without asking

- Do NOT alter code logic, behavior, or code-line formatting — comments only.
- Do NOT rewrite comments outside the requested scope.
- Do NOT add comments to files where the project forbids them or where they break the build.
- Do NOT `git commit` or `git push` unless explicitly told to.
- Report what you rewrote and what you deleted, with the reason for each deletion.
