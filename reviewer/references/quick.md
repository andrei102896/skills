# Quick — a fast pass on work in progress

`/reviewer quick [--base <branch>]`: one agent, the branch plus uncommitted edits, changed lines only. No walkthrough,
no zones, no findings file, no triage, no verify.

## Prep

Run `python3 -B <skill dir>/scripts/prep.py --quick [--base <branch>]`.
- `STOP: <reason>` → explain in one line and stop.
- Keep `base:` and `range:` (with `--quick` the head is a snapshot of the working tree, so uncommitted edits are
  included and no `UNCOMMITTED` question is asked) and the `prior findings:` block.
- Keep `files: <n>` for the closing line. Ignore `walkthrough:` and `ZONES REQUIRED`.

## One agent

Launch one fresh `general-purpose` agent with `model: "opus"` and `effort: "medium"` (never a fork, never another
model). Brief: the cwd, the range, the earlier findings answered **not valid** copied word-for-word from the prior
files, and these instructions:

> A quick review of work in progress, changed lines only.
> 1. Load only the quick rules: for each `<skill dir>/rules/*.md` with `quick: true` in its frontmatter (a project file
>    of the same name in `.claude/review-rules/` replaces it), read it with
>    `awk 'FNR==1{s=0} /^\*\*Seen/{s=1;next} /^\*\*/{s=0} !s' <file>`; also read `<skill dir>/rules/_do-not-flag.md`
>    and the project's one if present. List them with `grep -l '^quick: true' <skill dir>/rules/*.md`.
> 2. Read `<skill dir>/references/evidence.md` and the label list in `<skill dir>/references/format.md`.
> 3. Read `git diff -U8 <range>`, with `sed -n` for surrounding context, several files per call.
> 4. Bugs first: null, empty and missing values, condition and index boundaries, a missing `await` or a swallowed
>    error, a race, cleanup on unmount or failure. Then the quick rules.
> 5. No repo-wide searches, and no Unused, one-caller or Duplicate claims: the work is not finished.
> 6. Each candidate passes its evidence row; never re-raise a **not valid** one; confirm every `file:line` with one
>    batched `sed -n` call.
> 7. Answer in exactly this shape, omitting empty headings, with no taste calls and no fixes:
>    **Findings** — `` `file:line` — **Label.** what is wrong and what it causes ``
>    **Questions** — `` `file:line` — **the one question** `` and what each answer means
>    **Bigger than this change** — one line each

## Output

Print the agent's answer as it is, or "nothing found in <n> files". Nothing is written, nothing is fixed.
