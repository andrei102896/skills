# Author mode — the author's own branch

The author reviews their own branch, usually before pushing. Same lens, same evidence and verification; the output is a
findings file the author never has to open: you walk them through it, record each answer, and fix what they accept.

## Before the review

- **Uncommitted edits** → one question naming their count and a few files: review them too, or stop so they can
  commit first. Never commit or stash for them.
- **Base**: the MR's target when an MR exists; otherwise the branch it was created from, guessed (`feature-x-y` →
  `feature-x`, else the integration branch). Say the base, and that it was a guess when it was.
- **Earlier rounds**: read every findings file of this branch first (see "Earlier rounds" in the skill). A file whose
  findings are not all answered is a resume: say "continuing <file>, <n> left" and go straight to triage on those.
  Edits already in the tree are the fixes made so far — never stash or question them.

## The findings file

Path: `~/.claude/reviewer-findings/<repo>/<branch>-<YYYY-MM-DD>-r<N>.md`, outside the repo and outside this skill
(`r<N>` = one more than the branch's last round). Header `# local <branch> → <base> — r<N> (<date>)`, then
`## Zones reviewed` (zones and file counts, or "whole branch (<n> files)") and the diff range, then sections A–D and
"Checked and clean". Ids are `<N>.<section><n>` (`1.A3`). Every finding in A–D, in English, speaking to the author
directly ("rename X"):

    - **1.A4. `path/to/file.ts:52`** — **Duplicate.** What is wrong and what it causes, one sentence.
      Evidence: the grep, the other call site, the line that contradicts it.
      - [ ] request change
      - [ ] not now
      - [ ] not valid

Verification pre-ticks section A only: `holds` → `[x] request change — **verify:** holds — <reason>`, `doubtful` or
`wrong` → `[x] not valid — **verify:** <verdict> — <reason>`. B, C and D are verified but left unticked. Never move or
delete a finding.

## Triage — the author decides, you record

Every answer is written to the file **at once** (that is what makes a re-run resume): an `x` in the box, then
` — **author:** <answer>` on that box line. A finding with no `**author:**` is undecided.

1. **Section A, one question**: "N proven fixes, each checked against the code, low risk: apply all / one by one", with
   one line each (`file:line`, label, what changes). Apply all → fix each, tick `request change — **author:** fixed`.
   A finding the verifier marked `doubtful` or `wrong` never goes in the batch: ask it one by one.
2. **Then each undecided finding, one question each**, in file order. The author has never seen the format, so the
   question's first line is the kind in words — "Proven fix (checked against the code)", "One question decides it",
   "Your call (taste, no right answer)", "Bigger than this branch (worth a talk with the team)" — and the second line
   opens with the label and id, then the problem in 2–3 lines (for B, the question in bold). Options:
   - **Fix it** → make the change, tick `request change — **author:** fixed`.
   - **Not now** → tick `not now — **author:** not now`.
   - **Not valid** → ask "why? (one line, optional)", tick `not valid — **author:** <reason>`.
   - **Explain and re-check** → re-read the code with fresh eyes. If it no longer holds, say why and tick
     `not valid — **author:** withdrawn — <why>`; otherwise explain it better and ask again without this option.
   An answer that says stop → stop; the next run resumes.
3. **End**: "fixed X, not now Y, not valid Z, withdrawn W", the files changed, and "review the diff, commit, push".
   Run the project's lint and focused tests on the changed files before saying the fixes are done.

## Feedback loop (`--learn`)

Answered findings files are how the rules improve. Read the branch's files back, newest first, and propose rule
changes; apply them only with the user's approval, and only to rules this user owns (the project's
`.claude/review-rules/` or a local rules clone). A rules source fetched read-only from someone else gets the proposals
as a list for its owner.

- **not valid** → add the case to that rule's `**Counter-example**` section, in the author's words when they gave a
  reason (the `**verify:**` text is the verifier's, not theirs). `withdrawn` is the strongest counter-example: the
  reviewer itself dropped the finding on re-check.
- **The same reason twice → narrow the rule, don't delete it.** Two rejections for one reason mark a boundary the rule
  does not know yet: write it in as a condition. Weigh the rejections against the rule's accepted findings and its
  `seen:`; propose deleting a rule only when the narrowed version would no longer fire on anything accepted, with the
  counts.
- **not now** → the finding was right, so it is not a counter-example; a rule that keeps getting "not now" is ranked
  too high, so propose narrowing when it fires.
- **request change in section B** → the question was the interesting part: if it recurs, its answer belongs in a rule
  so the next review does not ask it again.
- Something the author flagged that no rule produced → add it to the closest rule, or a new one if it recurs.
- One author's taste weighs less than the rule owner's: a rule changes from an author's rejections only when they recur
  across authors. Bump `seen:` only on a re-harvest, never from one review.
