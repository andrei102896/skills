# Worktree — review a PR without touching the user's checkout

The walkthrough needs the working tree to be the reviewed head. When the user's checkout is on another branch or has
edits, review the PR in a separate worktree instead of switching anything. Create one only with `--worktree` or when
the user asks; never in author mode or with `quick`.

## Set it up

- `MAIN` = `git rev-parse --show-toplevel` at the start of the session; `<repo>` = its basename.
- Get the PR's head branch: `gh pr view <n> --json headRefName -q .headRefName`.
- `git fetch origin <branch>`.
- Directory `../<repo>-pr-<n>` next to `MAIN`:
  - missing → `git worktree add --detach ../<repo>-pr-<n> origin/<branch>`;
  - present and at `origin/<branch>` → reuse it;
  - present at an older commit → `git -C ../<repo>-pr-<n> checkout --detach origin/<branch>`.
- Never change `MAIN`'s branch or files.

## Inside it

- Run `prep.py` and the `walkthrough:` command with the worktree as cwd, and give every agent the worktree path as its
  cwd. Every `sed -n` line check reads the worktree's files, not `MAIN`'s.
- Callers outside the diff come from the walkthrough's `git grep` and the language server; a language server bound to
  `MAIN` sees `MAIN`'s code, so in the worktree prefer grep plus `goToDefinition` and say so in the findings header.
- Findings and the index are filed under `<repo>` (the main checkout's name), so `/reviewer` on the branch in `MAIN`
  resumes the same file.
- `usage.py` runs from `MAIN` (session transcripts are keyed by the session's start directory).
- `--fix-a` edits the worktree. Say so at close, with the worktree path.

## Afterwards

Never remove the worktree. At close tell the user: `git worktree remove ../<repo>-pr-<n>` when they are done.
