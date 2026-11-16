# Judge — one agent per rule group, in parallel

One context checking every hunk against every rule skips rules the further it reads. So the diff is judged by several
agents at once, each holding a short rule list.

## Who runs

- One agent per row of the walkthrough's `## Groups` table whose hunks are not `none — skip`. Take each group's name,
  rules and hunk ids from that table word-for-word; do not restate or re-route them.
- Plus one **delivery** agent, always: lens checks 1, 4, 9, 10 and 11 from the skill, over the whole change.
- Project rules: a file in the project's `.claude/review-rules/` with the same name as a built-in rule replaces it.
  Project rule files named in no `## Groups` row go to one extra agent, group `other`, over all hunks. When the table
  already has an `other` row, use that row instead.
- A very large group (more than ~60 hunks) may be split into slices by area, one agent each, same rules.

Every agent is a fresh `general-purpose` agent launched with `model: "opus"` and `effort: "medium"`, never a fork and
never another model. All of them go in **one message** so they run in parallel.

## The brief

Each brief holds, and nothing else:
- the cwd (in a worktree, the worktree path), the diff range from prep's `range:` line, the walkthrough index path;
- the group name, its rules, its hunk ids;
- the earlier rounds' findings answered **not valid** and the still-open **request change** ones, copied word-for-word
  from the files in prep's `prior findings:` block, with their `**author:**` / `**verify:**` text;
- PR mode: the `pr:` line and the `pr comments:` block word-for-word; any `stacked:` lines (both modes);
- the instructions below;
- correctness: lens sections 0, 2, 3, 5, 6, 7, 8 and both procedures of [gather.md](gather.md) ("callers of changed
  contracts", "readers of changed data");
- delivery: lens sections 1, 4, 9, 10, 11, the blind-spot list, and the commands for the change as a whole:
  `git log --format='%h %s%n%b' <range>`, `git diff --stat <range>`, and in PR mode
  `gh pr view <n> --json title,body,commits`.

Pass the lens sections by telling the agent to read them:
`awk '/^## Lens/{p=1} /^## Blind spots/{p=0} p' <skill dir>/SKILL.md`, and for the blind spots
`sed -n '/^## Blind spots/,$p' <skill dir>/SKILL.md`.
Never pass your own reading of the diff: each agent forms its findings from the code.

## Agent instructions (paste into every brief)

> You review one slice of a change: the **<group>** rules on hunks <ids>. Other agents cover the other rules at the
> same time, so stay on yours.
> 1. Learn the project's own conventions first: `package.json` (or the stack's manifest), `AGENTS.md` / `CLAUDE.md`
>    at the root and nearest the touched files, and the closest sibling of each touched file. Judge against those.
> 2. Load your rules once. For each rule `<r>`: the project's `.claude/review-rules/<r>.md` if it exists, else
>    `<skill dir>/rules/<r>.md`; read it with
>    `awk 'FNR==1{s=0} /^\*\*Seen/{s=1;next} /^\*\*/{s=0} !s' <file>` (drops any quote list). Also read
>    `<skill dir>/rules/_do-not-flag.md` and the project's `.claude/review-rules/_do-not-flag.md` if present: both and
>    every rule's counter-examples are binding.
> 3. Read `<skill dir>/references/evidence.md` and the finding shape and label list in
>    `<skill dir>/references/format.md`.
> 4. Read the walkthrough index. For your hunks read the code: `git diff -U8 <range> -- <file>` and the function
>    around it with `sed -n`. Batch several files per shell call, never one per turn.
> 5. Judge changed lines only, against your rules only. A `facts:` lead is a grep result: confirm it in the code. A
>    real bug outside your rules: report it anyway, labelled **Bug**.
> 6. Drop anything already raised in the PR comments, answered **not valid** earlier, or covered by the do-not-flag
>    file or a counter-example. Before any Unused or Dead code finding, grep each `stacked:` branch:
>    `git grep -n -w '<symbol>' origin/<branch>`.
> 7. Every candidate passes its row in the evidence table or is dropped. Confirm every `file:line` with one batched
>    `sed -n` call before answering; never compute a line from a hunk header.
> 8. Answer with findings only, each preceded by its section letter (A/B/C/D), in the format.md shape without id and
>    without boxes, then a "Checked and clean" list (one line each). No findings is a fine answer. Never write a fix.

## The groups

The rule lists live in the `## Groups` table; this is what each group is for.

| Group | Focus | Hunks |
|---|---|---|
| correctness | the bug hunt, changed contracts, changed data, untrusted input | all |
| existence | does this code need to exist today; delete instead of keep; reuse before adding; inline single-use helpers | all |
| form | simpler form, weak types, naming, magic values, pass only what is needed | all |
| structure | comments say why, file placement, one convention per file, logic at the right level, lint suppressions, scope and rollout | all |
| ui | UI patterns, the project's building blocks, state and data flow, translation keys | routed |
| backend | migrations, logging, resource lifecycle, API layer conventions | routed |
| delivery | description, commits, docs, tests, siblings, tunables, dependencies (not a table row) | the whole change |

## Merge

When every agent has answered:
- the same `file:line` with the same problem from two agents becomes one finding, the one with the better evidence;
- a two-part finding is split into its A part and its C part;
- an agent that failed or returned nothing usable is named in the findings header: its rules were not checked this
  pass. Do not rerun it silently;
- "Checked and clean" lines are kept, one per checked item.

Then write the file ([format.md](format.md)) and verify ([verify.md](verify.md)).
