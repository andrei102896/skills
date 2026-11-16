---
seen:
label: Dead code
quick: false
---
# Justify this code

Ask whether each added piece needs to exist, and name the specific condition that makes it unnecessary.

**Finding when the diff adds:**
- a guard that is always true, or a fallback for a value that is never absent;
- a boolean passed down and checked again where it is always true;
- a flag or ref that is set once and never changes;
- an unused parameter, or a whole object passed where two fields are read;
- an effect that repeats what the side-effect layer or a selector already does;
- an abstraction justified only by a future need.

**Section by where the guarantee lives:**
- guarantee in the same flow (the caller always passes it) → section A: the guard goes, the type gets tighter;
- our own data written by another writer → section B: ask; the guard is legitimate with a comment saying why;
- a trust boundary (user input, network, storage, third party) → not a finding.

Guards that survive should skip the bad item and log, or throw; never silently default.

**Counter-example**
- Never ask to replace a dead guard with a silent fallback: it ships empty values instead of dropping bad items.
- A check that only narrows `T | undefined` after a map or dictionary lookup is type narrowing, not dead code.
