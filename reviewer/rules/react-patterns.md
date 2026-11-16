---
seen:
label: Convention
quick: true
---
# Component patterns

Component and hook code follows the idioms of the project's UI framework. Read the closest sibling component first.

**Finding when:**
- memoization does not earn its place: callback chains that exist only to satisfy dependency lists, memo over a
  trivial expression, memo over a freshly converted copy, refs holding what a local variable or a cleanup could hold,
  duplicate refs to the same thing (dependency-list warnings are guidance, not law);
- a wrapper only forwards to a handler that could be passed directly;
- a component is defined inside another component, or one file holds several components;
- state mirrors props or the store instead of being derived at render;
- an effect adds a listener and removes a different function reference (define the handler inside the effect), leaves
  a timer running, measures layout in a post-paint effect when a pre-paint one exists, or repeats work a selector or
  the side-effect layer already does;
- a component calls the network directly when the project routes IO through its side-effect layer;
- long derivation sits in the component instead of a selector or helper;
- async UI has no loading state or no visible failure ("what does this show when the request fails?");
- the DOM is queried directly instead of through a ref;
- inline style is used where the project's styling mechanism should be, except for per-instance or per-render dynamic
  values; and those dynamic values do not belong inside a static styled template (continuous numeric props there
  generate a new class per value);
- the UI renders something the user cannot access instead of not mounting it.

**Counter-example**
- Memoization with a measured or evident cost (a large list, an expensive computation, an identity a child relies on).
