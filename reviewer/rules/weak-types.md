---
seen:
label: Weak type
quick: true
---
# Weak types

Types say what the runtime guarantees.

**Finding when:**
- a type marks everything optional while the runtime always provides the fields;
- a new local type restates an existing domain type;
- a union is undecided (`string | number` for an id) instead of picking one;
- casts are chained to force a shape;
- a new `any` (or the language's equivalent escape hatch) appears;
- a helper is typed narrower than what its callers actually pass;
- a function returns `T | null` or `T | undefined` where a default parameter, a throw, or an always-valid value would
  do.

**Known exception:**
- An untyped catch variable in existing code is tolerated; it is a separate migration task.
