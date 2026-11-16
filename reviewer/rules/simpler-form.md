---
seen:
label: Too complex
quick: false
---
# Simpler form

Same logic, shorter form. Always name the concrete construct to use.

**Finding when the diff could use:**
- a language built-in instead of hand-written code: deep clone, a set type (and keep it a set), one pass instead of
  two, map/find/filter for their meaning with reduce only to accumulate, an async iteration form instead of a
  suppressed await-in-loop warning;
- the data layer's single update or count helper instead of find-then-save or load-then-count;
- layout CSS (centering, gaps) instead of computed positions;
- control flow cleanup: hoist calls common to both branches, build the object then call once, merge duplicate guards,
  a two-value switch as if/else, a flattened nested switch, one try/catch around a switch, early returns instead of
  flag variables and a trailing return;
- smaller expressions: a plain truthiness check, conditional rendering with a short-circuit, no needless async,
  resolved-promise wrapper or template string, destructuring instead of index access.

**Counter-example**
- Forms the project's linter already enforces: then the finding is that the local linter is not running.
- Rewrites that change behavior (a set drops duplicates the list kept).
- An unusual but working implementation is a question, not a demand.
