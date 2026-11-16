# Verify — a fresh context checks every finding

A reviewer re-reading its own list never drops what a rule made fire; a fresh agent asked "does this hold?" does.
Run this whenever the findings file has at least one finding in A–D.

## Launch

- One fresh `general-purpose` agent per changed file that has findings; with many small files, group neighbouring
  files so there are at most about eight agents.
- Each launched with `model: "opus"` and `effort: "medium"`; never a fork, never another model.
- All in **one message**.

## The brief

Give each agent only:
- the findings for its file(s), copied word-for-word from the findings file (id, label, sentence, evidence);
- the file paths, the cwd and the diff range;
- for each finding's label, the rule file behind it (the project's `.claude/review-rules/<r>.md` when it exists, else
  `<skill dir>/rules/<r>.md`), plus `<skill dir>/rules/_do-not-flag.md` and the project's one if present;
- `<skill dir>/references/evidence.md`.

Never give it your reasoning, the walkthrough, the agents' answers or this conversation.

Ask it, per finding:
> Argue both sides. What would have to be true in the code for this finding to be wrong? Check whether that is true:
> read the cited lines, the callers, the types, the do-not-flag file and the rule's counter-examples. Answer one line
> per id: `holds`, `doubtful` or `wrong`, then a one-line reason. `doubtful` and `wrong` must cite a `file:line` or a
> grep you ran. Never suggest a fix.

## Record the verdicts

Edit the findings file once, all edits in one message.

- **Section A** is pre-ticked:
  - `holds` → `- [x] request change — **verify:** holds — <reason>`
  - `doubtful` or `wrong` → `- [x] not valid — **verify:** <verdict> — <reason>`
- **Sections B, C, D** are verified but never pre-ticked and get no verify text; their `doubtful` / `wrong` ids are
  only reported in the terminal.
- Never move, reword or delete a finding.

Gate: every finding has a verdict. An agent that failed → say which findings went unverified in the terminal and in
the header; do not tick them.

At close, the terminal counts include the ids found `doubtful` or `wrong`, by section.
