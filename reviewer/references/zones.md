# Scope — zones for diffs over 30 files

A diff over 30 files read in one pass gets the same shallow read everywhere, and the files nobody chose are where the
bugs survive. So prep prints `ZONES REQUIRED` and the review covers the zones the user picks, a pass at a time. With
30 files or fewer, skip this file: the whole diff is one pass, no question.

## 1. List the zones

Run prep's `walkthrough:` command with `--zones` added. It writes nothing and prints the title and file count, then one
block per zone, biggest first: the file count, the zone's path prefix, up to six of its files and `… <k> more`. Zones
under four files are pooled into a final `scattered` zone.

Read the `## Zones reviewed` section of every findings file listed in prep's `prior findings:` block for this branch.
Show the zone list with the zones not reviewed yet first, each marked "(not reviewed yet)". When every zone is already
covered, say so and ask whether to review them again before going on.

## 2. Ask once

One AskUserQuestion with two `multiSelect: true` questions:
1. **Zones for this pass** — options = the largest zones (not-reviewed ones first); free text allowed for any other
   prefix.
2. **Extra focus** beyond the rules — e.g. correctness, security, resources and limits, delivery.

Never pick the zones yourself and never start gathering before the answer. Stop and wait.

## 3. Review the picked zones in one pass

- Run the walkthrough with one `--zone <prefix>` per picked zone, all in the same command, so a caller in one zone and
  its callee in another are read side by side. An unknown prefix fails with "no files in zone": rerun `--zones` and
  ask again.
- Pass the extra focus to every agent brief as one line ("extra focus: …").
- One findings file per pass. Its `## Zones reviewed` section lists each zone prefix with its file count, and the diff
  range.
- An outside caller in the index may live in an unpicked zone of the same change; the agents treat it like any other
  outside caller.

## 4. Afterwards

At close, list the zones still not reviewed and offer the next pass: `/reviewer` again reviews the remaining zones
first (after triage of this file, since an undecided file resumes instead).
