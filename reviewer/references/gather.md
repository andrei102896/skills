# Gather — the walkthrough index

The main thread reads an index of the diff, not the code. The agents read the code.

## Run it

Run the exact command from prep's `walkthrough:` line. When zones were picked, append one `--zone <prefix>` per zone.
The index is written to `~/.cache/reviewer/<repo>/walkthrough/<name>.md` (`<name>` = the branch, plus
`--<zone>+<zone>` when zoned) unless `-o <path>` is given. A non-zero exit with a message about the checkout means the
working tree is not the reviewed head or has local edits in its files: explain, offer `--worktree` in PR mode, stop.

Read the index once, in full. Keep its path and its `## Groups` table for the briefs; do not read code in the main
thread.

## What the index holds

- Files in **call order**: a caller before the files it imports, so a caller and its callee are read together.
  `Calls into, later in this review:` names the in-diff files a file imports.
- Hunks numbered `H1…Hn` across the whole diff: `` `<path>:<start>-<end>` ``, the enclosing symbol when git gave one,
  and `+added −removed`. A hunk range locates the hunk, never a line: read the line before citing it.
- **Outside callers** under each file: files outside the diff that import it and name a changed export (found with
  `git grep -w` at head, then confirmed by the import path, relative or through the repo's path aliases, up to two
  re-export hops). Generic names are skipped with a note. That list is where bugs a diff view hides live; it is a lead,
  not a verdict. With `--zone`, a caller may sit in an unpicked zone of the same change.
- `**Still import what this change removes**` under a file: files that import a name the diff deleted from it.
- `> **check:** <rules>` lines: the rules routed to a hunk by its file kind and content.
- `> **facts:**` lines tagged `[one-caller]`, `[unused-export]` or `[one-importer]`: grep results to confirm in the
  code, never findings by themselves. A default export is not reported by name; JSON, config and test files count as
  uses.
- `## Groups`: one row per rule group, its rules, and its hunks (`all (H1–Hn)`, a list, or `none — skip`). This table is
  the single source of which agent gets which rules and hunks.
- `## Tests in this diff`: test files with their counts; not inlined, read by the agents as evidence.

Reading code (agents): a hunk with context via `git diff -U8 <range> -- <file>`, surrounding code via
`sed -n '<a>,<b>p' <file>`, several files per call.

## Correctness agent — callers of changed contracts

1. Pick the changed symbols whose **contract** changed: a parameter added, removed, reordered or made required; the
   return shape; a field accepted or returned renamed or dropped; a new throw; a rename or deletion. Body-only changes
   are not contracts. Usually 0–5; above 10, prefer those with outside callers in the index.
2. Find the call sites with the language server: `prepareCallHierarchy` then `incomingCalls` for functions,
   `findReferences` for types, constants and components. Trust a complete language-server search only for files
   inside a project the server loads (a `tsconfig.json`/`jsconfig.json` or the language's equivalent); elsewhere grep
   `<name>(` and run `goToDefinition` on each hit to drop namesakes. For languages without a server, use the index's
   outside callers plus grep. Never trust a grep count for generic names (get, set, map, t, it, dispatch).
3. A call site still on the old contract → **Bug**, or **Rollout** when the caller is in another deployable that ships
   separately. Evidence: the caller's `file:line` and the argument or field that no longer matches.
4. All callers updated → one "Checked and clean" line: `` `name` — N callers, all updated ``.
5. No language server available → fall back to grep and say so; the findings header records it.

## Correctness agent — readers of changed data

When the diff adds an enum or type value, a new row or document kind, or a new secret (hash, token, code) to an
existing table, collection or store, no call graph links the old readers to the new rows. Grep the model name, the
table or collection name and the matched field across every backend directory, then check that each query filters by
the type or status that tells the new rows apart.

- A reader matching the new rows by a shared value (only by hash, only by id) → **Security** when it touches auth,
  sessions, passwords or permissions; **Bug** otherwise.
- Evidence: the reader's `file:line` and its filter, plus the diff line that writes the new rows.
- Every reader safe → "Checked and clean": `` `<table>` — N readers, all filter by type ``.

Motivating case: a change added a "magic link" row kind to an existing `login_tokens` table and put its hash in a
token the client could read. An older lookup selected rows by hash alone to finish a password reset, so it matched
the new rows too: anyone holding the readable token could reset the account's password. Nothing in the diff touched
that lookup; only grepping the table's readers found it.
