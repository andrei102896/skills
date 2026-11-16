---
seen:
label: Hardcoded value
quick: true
---
# Magic values

Meaningful literals have a name and one source.

**Finding when:**
- a meaningful number, string, duration, size or limit is written inline instead of as a named constant;
- an equivalent already exists (theme token, design-system value, another module's constant, config) and the diff
  writes the literal instead; cite the existing source;
- the job is half done: one group of values got constants and its neighboring group did not;
- layering, breakpoint, spacing or color values bypass the design-system source the project has.

**Not a finding:**
- 0, 1, -1, empty string and similar values whose meaning is obvious from the expression;
- literals in tests and fixtures.

**Counter-example**
- A value used once whose meaning is clear from a well-named variable it is assigned to.
