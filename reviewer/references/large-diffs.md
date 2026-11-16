# Large diffs — zones and parallel rule groups

A diff over 30 files read in one pass gets the same shallow read everywhere, and the files nobody chose are where the
bugs survive. One context checking every hunk against every rule also skips rules the further it reads. So a large diff
is split twice: by zone (what to read) and by rule group (who reads it).

## 1. Zones

- Group the changed files by path into logical zones (`services/billing/`, `web/app/settings/`, `packages/shared/`),
  biggest first, with a `scattered` bucket for one-off files. Show the list.
- Ask once, both multi-select: which zones this pass covers, and what to focus on beyond the rules (correctness,
  security, resources and limits). Never pick the zones yourself and never start before the answer.
- Review the picked zones together in one pass, so a caller in one zone and its callee in another are read side by
  side. The findings file lists them under `## Zones reviewed`; the next run offers the zones not reviewed yet first,
  until every zone is covered.

## 2. The index

Build an index of the diff, not the code: every hunk gets an id (`H1`…), its `file:start-end`, the enclosing symbol and
its +/− counts, in **call order** (a caller before its callees), so a caller and its callee are never reviewed apart.
Under each file, list its callers from outside the diff (language server or grep) — that is where the bugs a diff view
hides actually are. Mark hunks with leads the diff cannot show (a helper with one caller, an export nobody imports),
labelled as leads from a grep, not verdicts. Keep the index in a file; the main thread reads only the index.

## 3. Rule groups

Route the hunks to a small number of groups, each with a short rule list:

| Group | Checks | Hunks |
|---|---|---|
| correctness | section 3.0 of the skill, plus the security rule | all — split into slices by area when the diff is large |
| existence | is this code needed today; delete instead of keep; reuse before adding; inline single-use helpers | all |
| form | simpler form, weak types, naming, magic values, pass only what is needed | all |
| structure | comments say why, file placement, one convention per file, logic at the right level, lint disables, scope and rollout | all |
| ui | framework patterns, component library, state management, i18n | UI files only |
| backend | migrations, logging, resource lifecycle, API conventions | server, worker and data files only |

Map the project's own rules (`.claude/review-rules/` or the profile's source) into these groups by their topic; a
group with no hunks is skipped.

## 4. Start them

All agents in **one message**, so they run in parallel. Each brief holds: the cwd, the diff range, the index path, the
group name, its rules and its hunk ids, the earlier rounds' **not valid** findings and the existing MR comments word
for word, and these instructions:

> You review one slice of a change: the **<group>** rules, on the hunks listed for you. Other agents cover the other
> rules at the same time, so stay on yours.
> 1. Load your rules once, without their quote lists, plus the do-not-flag file and each rule's counter-examples.
> 2. Read the index. For your hunks read the code: the diff with context, and the function around it. Batch several
>    files per shell call, never one per turn.
> 3. Judge only changed lines, against your rules only. A lead in the index is a grep result: confirm it in the code.
>    A real bug you notice outside your rules: report it anyway, labelled **Bug**.
> 4. Every candidate passes its row in the evidence table, or is dropped. Confirm every `file:line` against the file
>    in one call before you answer.
> 5. Answer with nothing but the findings, each preceded by its group (A/B/C/D), without ids, then a "Checked and
>    clean" list. No findings is a fine answer.

The correctness agent(s) also get section 3.0 in full: the bug hunt, exact callers of changed contracts and existing
readers of changed data. Never give an agent your own reading of the diff: each one forms its findings from the code.

## 5. Merge

When every agent has answered: the same `file:line` and the same problem from two groups becomes one finding, the one
with the better evidence. An agent that failed is named in the findings header: its rules were not checked this pass.
Then number, write and verify as usual.

Keep the main thread small: every turn re-reads the whole context, so context size × turns is the cost. The code is
read by the agents; batch whatever does not depend on the previous result into one message.
