# Format — the findings file

## Where

The path from prep's `findings file: <path> (r<N>)` line:
`~/.claude/reviewer-findings/<repo>/<branch with / → ->-<YYYY-MM-DD>-r<N>.md`. It lives outside the repository and
outside the skill; `r<N>` is one more than the branch's highest earlier round. Never write it anywhere else.

## Shape

```
# local <branch> → <base> — r<N> (<YYYY-MM-DD>)          # author mode
# #<pr> <branch> → <base> — r<N> (<YYYY-MM-DD>)          # PR mode

## Zones reviewed
- whole branch (<n> files)                                # or one line per zone: `<prefix>/` — <n> files
- range `<base8>..<head8>`
- not checked: <group> (agent failed) · callers: grep fallback, no language server · carried over from <file>
                                                          # only the parts that apply; omit the line when none

## A. Proven fix (checked against the code)
## B. One question decides it
## C. Your call
## D. Bigger than this branch
## Checked and clean
- <what was looked at and holds, one line each>
```

Empty sections are omitted, except "Checked and clean", so silence is legible. The usage section is appended at close
by `usage.py`; never write it by hand.

## Finding

```
- **<N>.<S><n>. `src/cart/CartPanel.tsx:52`** — **<Label>.** <one standalone sentence: what is wrong and what it causes>
  Evidence: <at most two concrete lines: the grep, the only caller, the line that contradicts it>
  - [ ] request change
  - [ ] not now
  - [ ] not valid
```

- **Ids** carry the round: `<N>` is the round from the file name, `<S>` the section letter, `<n>` its position in the
  section (`2.A1`, `2.B3`). Ids never repeat within a branch.
- **Section A** — mechanical: proved, the author confirms in seconds. Problem plus proof.
- **Section B** — the one question, in bold, then what each answer means:
  ```
    **Can the backend send `status: "partial"` here?**
    - If yes: an accepted risk the spec must list.
    - If no: a dead branch — the `partial` case in line 88 never runs.
  ```
- **Section C** — the tradeoff in one line: the other shape and what it costs.
- **Section D** — what is structurally wrong and where the decision belongs; propose a discussion, never a redesign.
- **Checked and clean** has no ids and no boxes.

Within a section, rank by blast radius: security, data loss, crash → wrong behaviour → missing sibling or consumer
update → limits and performance → hygiene. Keep A hygiene items to about five.

## Writing rules

- **Labels** (closed list): Bug, Duplicate, Unused, Dead code, Too complex, Wrong comment, Weak type, Misplaced,
  Naming, Inconsistent, Hardcoded value, Too broad, Convention, Resource, Security, Lint disabled, Design system,
  Rollout, Question. Default = the fired rule's `label:`; never invent one.
- **No fix.** No `Fix:` lines, replacement code, "consider…" or "you could…". Naming an existing helper's path is
  evidence.
- **Self-contained.** A finding never points at another finding ("same as A2"), another zone or this review's own
  vocabulary; repeat the fact or the `file:line`. Use names the author recognises.
- **Address the author directly** in author mode ("this ref is never read").
- **Unproven** → say "suspected" and put it in B.
- English only. Each paragraph at most three lines.

## Boxes and suffixes

Exactly one box is ticked per decided finding, and the decision is appended to that same line:

- ` — **verify:** <holds|doubtful|wrong> — <reason>` — written by verify, section A only
  (holds → `request change`, doubtful or wrong → `not valid`).
- ` — **author:** <answer>` — written in triage or by `--fix-a`: `fixed`, `not now`, `<reason>` or
  `withdrawn — <why>`. When the author picks another box than verify did, clear verify's `x` (its text stays on its
  line) and tick the chosen box with the author suffix, so exactly one box stays ticked.

```
  - [x] request change — **verify:** holds — the only reader is line 40 — **author:** fixed
  - [ ] not now
  - [ ] not valid
```

A finding with no `**author:**` suffix is undecided; a file with an undecided finding makes the next `/reviewer` on
this branch resume it. Never move or delete a finding.
