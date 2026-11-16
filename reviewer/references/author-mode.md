# Triage — the author decides, you record

The author reviews their own branch, usually before pushing. They never have to open the findings file: you walk them
through it, record each answer, and fix what they accept. Runs after close in author mode, and directly when prep
printed `RESUME <file>: <ids>` (then only those ids, in that file).

## Recording

Every answer is written into the file **at once**, before the next question: that is what makes a stopped run resume.
Tick the chosen box and append ` — **author:** <answer>` to that box line, following the box rules in
[format.md](format.md). A finding with no `**author:**` suffix is undecided. Never move, reword or delete a finding.

## 1. Section A, one batch question

Collect the section A findings whose verify verdict is `holds` and that have no author answer. If there are any, one
AskUserQuestion, header `Proven fixes`:

> N proven fixes, each checked against the code, low risk — apply all, or go one by one?

with one line per fix: `file:line`, label, what changes. Options:
- **Apply all** → make each change, then append ` — **author:** fixed` to its `request change` line.
- **One by one** → they join step 2.

Findings the verifier marked `doubtful` or `wrong` never go in the batch: they are asked one by one in step 2.

## 2. Each remaining undecided finding, one question

In file order, one AskUserQuestion per finding. Header chip by section: A `Proven fix`, B `Question`, C `Your call`,
D `Discuss`. The question text:

- first line, alone — the section in words: A "Proven fix (checked against the code)", B "One question decides it",
  C "Your call (taste, no right answer)", D "Bigger than this branch (worth a separate look)";
- second line — `<Label> · <id> — <file:line>: <problem>`;
- then 2–3 lines of the problem and its evidence; for B, the one question in bold and what each answer means.

Options:
- **Fix it** → apply the change, then tick `request change — **author:** fixed`.
- **Not now** → tick `not now — **author:** not now`.
- **Not valid** → ask "why? (one line, optional)", tick `not valid — **author:** <reason>` (`no reason given` when
  empty).
- **Explain and re-check** → re-read the code with fresh eyes. If the finding no longer holds, say why and tick
  `not valid — **author:** withdrawn — <why>`. Otherwise explain it better and ask again without this option.

Free text that means stop ("stop", "later", "enough") → stop at once; the next `/reviewer` resumes from the first
undecided finding.

## 3. Fixing

- A fix touches only what the finding names. Read the code again before editing; the tree may have moved since.
- After the last fix, run the project's lint and the focused tests for the changed files (commands from
  `package.json`, `AGENTS.md` / `CLAUDE.md`). A failure caused by a fix is fixed or reported; a pre-existing failure
  is reported as pre-existing.
- Never commit, push or stash.

## 4. End

Print one line: "fixed X, not now Y, not valid Z, withdrawn W", then the files changed, then "review the diff,
commit, push". When zones remain unreviewed, say which and that the next `/reviewer` offers them first.

## Resume

On `RESUME <file>: <ids>`: say "continuing <file>, <n> left", skip phases 2–7, and run steps 1–4 on the
listed ids only. Edits already in the working tree are the fixes made so far: never stash, revert or question them.
