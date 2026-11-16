# Evidence — what each finding needs before it is reported

A candidate that cannot show its row's evidence is dropped, not softened. A concern that is likely but unproven goes
to section B as a question, never to A as a fact.

| Label | Needed | Not a finding when |
|---|---|---|
| **Duplicate** | the path of the existing constant, type or helper (grep or language server) | no path, or sharing needs a new helper with a mode or parameter because the copies feed different consumers or data |
| **Unused**, **Dead code** | a grep with no caller or setter; with `stacked:` branches, also `git grep -n -w '<symbol>' origin/<branch>` on each, named in the evidence | any stacked branch uses it |
| **Dead code** (guard) | the line that enforces the invariant: same flow → A, another writer of our data → B | the guard sits at a trust boundary, or only narrows `T \| undefined` from a lookup |
| **Bug** (changed logic) | `file:line`, the concrete input or sequence that reaches it, and the wrong result or crash | the types, a guard or the only caller make that input impossible (cite the line) |
| **Bug** / **Rollout** (changed contract) | the caller's `file:line` and the argument or field that no longer matches | every caller is updated → a "Checked and clean" line |
| **Security** / **Bug** (changed data) | the existing reader's `file:line` and its filter, plus the diff line that writes the new rows | every reader filters by the new type or cannot match the new rows |
| **Too complex** | the simpler construct, named (a `Set`, one update call, one object built once) | a linter already enforces the form, or the rewrite changes behaviour |
| **Design system** | the project's own component, theme value or token that was bypassed (its path) | the page is still on a legacy layer kept until migrated, or the value is truly one-off |
| any other | the line plus the rule's condition | `_do-not-flag.md` or the rule's counter-example covers it |

## Always

- **Rounds.** A finding answered **not valid** in an earlier round is never raised again, even on new code. One
  answered **request change** that is still present is carried over, and the header names the file it came from.
  **not now** comes back only when the new code makes it worse.
- **Already raised.** Anything already in the `pr comments:` block, by a person or a bot, is not a finding.
- **Lines are read, not computed.** Every cited `file:line` is confirmed against the reviewed revision with one batched
  `sed -n '<line>p' <file>` call. A hunk header or an index range gives the hunk, never the line.
- **Count uses.** Put the count in the evidence: "the only caller passes two arguments", "the only reference is
  line 108". Search for a third copy before reporting two.
- **Scale with the codebase's numbers.** Quote the constant or limit that sizes the risk.
- **Architecture goes to D.** Name what is wrong and where the decision belongs; no redesign, not even one line.
- **Split two-part findings**: the provable half is A, the taste half is C.
- **Lint-owned forms.** When a lint rule already covers the form, say the rule applies, or drop it.
