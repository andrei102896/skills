---
seen:
label: Duplicate
quick: false
---
# Reuse before adding

Before a new constant, type, hook, client or utility is added, look for the existing one and name it.

**Finding when:**
- the diff adds something an existing module already provides and the existing one is usable as is (cite its path);
- two files are identical, or two modules hold constants with the same value and meaning;
- both copies encode the same domain rule, so they will drift.

**Counter-example**
- Code that only looks alike.
- Sharing would need a new helper with a mode or parameter because consumers or data shapes differ: the copy is
  cheaper than the merge, so it is not a finding.
