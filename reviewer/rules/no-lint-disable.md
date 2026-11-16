---
seen:
label: Lint disabled
quick: true
---
# No lint suppression

Every added suppression comment is challenged with the concrete fix. This covers any linter or type checker in any
language: next-line, block and file-level disables, type-checker ignore and expect-error directives, and inline
"allow" or "no quality check" markers.

**Finding when the diff adds a suppression for:**
- awaits in a loop that do not depend on each other → run them in parallel and wait for all; if the order is truly
  required, keep the loop with the suppression and a why comment, and do not hide it behind a different loop form;
- a restricted import → fix the import;
- a type-checker ignore on a third-party module → install its types or type the value;
- a hook dependency warning → fix the dependencies;
- a whole file → never acceptable.

**Counter-example**
- A suppression that already existed and was only moved, or sits near the diff, is out of scope.
- A suppression with a comment explaining a real constraint: ask whether the comment still holds.
