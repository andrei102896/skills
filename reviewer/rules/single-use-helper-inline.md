---
seen:
label: Too complex
quick: false
---
# Single-use helper: inline it

A function, constant or style object with exactly one caller in the same file (or in a sibling file created just for
it) is inlined. Extract on the second caller. When extraction is warranted, it goes to its own file, not to a private
helper just above the caller.

**Counter-example**
- A helper extracted only to satisfy a complexity limit is still a finding; say so.
- A helper with two or more real callers is fine, even in the same file.

**Yields to file-placement:** when helpers bury a component or hook at the top of its file, report it as Misplaced
instead. Helpers already moved to a sibling helpers file are fine.
