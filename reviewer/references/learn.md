# Learn — rules improve from answered findings

`/reviewer --learn [branch]` reviews nothing. It reads the answered findings files of a branch (default: the current
branch) and proposes rule changes; nothing changes until the user approves.

## Read

- Files: `~/.claude/reviewer-findings/<repo>/<branch with / → ->-<YYYY-MM-DD>-r<N>.md`, exact branch match (a branch
  that only starts with the same words is a different branch), newest round first.
- Only findings with an `**author:**` suffix count. Undecided ones are skipped; say how many.
- For each finding, find the rule behind it: the label's default rule, or the rule named in the walkthrough's
  `check:` line for that hunk when it is still in the cache. When unclear, ask instead of guessing.

## Which rule file changes

- The rule the review actually loaded: the project's `.claude/review-rules/<r>.md` when it overrode the built-in one,
  else `<skill dir>/rules/<r>.md`.
- `<skill dir>` is a shared skill that other repositories use too. Everything written there is **neutral**: describe
  the case in generic words with invented names (`src/cart/CartPanel.tsx`, an `orders` table); never a path, symbol,
  product, person or quote from the reviewed repository. Project-specific lessons go to the project's
  `.claude/review-rules/` instead (create the file with the same frontmatter when it does not exist).

## What each answer teaches

- **not valid** → add the case to the rule's `**Counter-example**` section, from the author's reason (the
  `**verify:**` text only when the author gave none). `withdrawn` is the strongest counter-example: the review itself
  dropped the finding on re-check. Skip a case the section already covers.
- **The same reason twice → narrow the rule, don't delete it.** Two rejections for one reason mark a boundary the rule
  does not know yet: write it into the condition. Propose deleting a rule only when the narrowed version would fire on
  nothing that was accepted, and show the counts (accepted vs rejected).
- **not now** → the finding was right, so it is not a counter-example. A rule that keeps getting "not now" is ranked
  too high: propose narrowing when it fires.
- **request change in section B** → the question was the useful part. When the same question recurs, its answer
  belongs in a rule so the next review does not ask it again.
- **verify said wrong, author agreed** → evidence that the rule's wording invites the false reading: propose sharper
  wording.
- Something the author fixed that no rule produced (a **Bug** outside the rules) → add it to the closest rule, or
  propose a new rule when it recurs across rounds or branches.
- Never change `seen:` from one review.

## Propose, then apply

1. Print the proposals as a numbered list: rule file, the exact text to add or change, and the findings that justify
   it (ids and the author's answers).
2. One AskUserQuestion (`multiSelect: true`): which proposals to apply. Do not edit before the answer.
3. Apply only the approved ones. A new built-in rule also needs its name in one `GROUPS` row of
   `<skill dir>/scripts/routing.py` (and a `CATEGORIES` row when that group is routed): put that line in the proposal
   and apply it with the rule, or the test below fails.
4. Run `python3 -B <skill dir>/scripts/test_walkthrough.py` after any rule file is added or renamed; it must print
   `ok`.
5. Report the files changed. Never commit or push; the user does.
