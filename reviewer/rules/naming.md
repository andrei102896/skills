---
seen:
label: Naming
quick: true
---
# Naming

Names state semantics and stay consistent with their neighbors.

**Finding when:**
- an abbreviation is used where well-named siblings spell the word out (or the reverse);
- the same value carries different names across files, or different values share one name;
- a name claims a false origin (a "server" value that is computed locally, a "cached" value that is not);
- a collection is not a plural, domain-accurate noun;
- a file that only holds data or types is named like an action (verb-first);
- a file with one function neither default-exports it nor is named after it;
- a generic name (`data`, `info`, `item`, `handle`) is used where the domain has a real word.

**Counter-example**
- Short names in a tiny scope where the meaning is obvious (a sort comparator's two arguments).
