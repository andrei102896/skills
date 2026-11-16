---
seen:
label: Inconsistent
quick: true
---
# One convention per file

Within a file (ideally a folder), each thing is done one way.

**Finding when the diff mixes, in the same file:**
- enums and string unions for the same kind of value;
- explicit return types on some functions and not others;
- object parameters and positional parameters for sibling functions;
- two ways of connecting components to shared state;
- arrow functions and function declarations (generator functions excepted);
- two ways of stopping event propagation;
- constants for one group of values and literals for its neighbor group;
- names that differ only by letter case;
- boolean names that do not start with `is` / `has` (or the file's prefix), or sibling names with different shapes.

**Counter-example**
- An inconsistency that predates the diff and the diff does not touch.
