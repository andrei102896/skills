---
seen:
label: Misplaced
quick: false
---
# File placement

Each kind of code lives where the project keeps that kind.

**Finding when:**
- a helpers folder receives constants or types; constants and types belong in their own folders or files;
- one file mixes kinds (component + constants + types + helpers) and should split by kind;
- business logic keeps growing inside one file instead of becoming a folder of small files;
- long inline logic sits in a component; it belongs in a helper file or a selector;
- a component or hook file does not start with the component or hook: helpers stacked above it (enough to scroll)
  move to a sibling helpers file. This takes precedence over single-use-helper-inline;
- a value that does not vary by environment lands in environment config instead of a constants file;
- the diff adds index or barrel files that only re-export, when the project does not use them.

**Not a finding:**
- placement that matches the closest sibling folder, even if another layout seems nicer.

**Counter-example**
- A small private helper below the component it serves, in a file that still reads top-down.
