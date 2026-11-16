---
seen:
label: Convention
quick: true
---
# State and data flow

State and derived data live where the project already keeps them, with no parallel copies. Before judging, learn the
project's own state layer (store, data containers, side-effect layer, selectors, cache): read `package.json`,
`AGENTS.md` / `CLAUDE.md` and the closest sibling file. Judge against that layer's own idioms.

**Finding when:**
- data is converted out of the state layer's own structures only to iterate or memoize it, when the layer's API
  already does that;
- model or slice defaults use a different data shape than the rest of the state;
- a selector or getter returns an unstable shape (sometimes missing, sometimes empty), forcing callers to guess;
- multi-line derivation of state happens in a component instead of a selector or derived getter;
- a custom hook that only reads state is not written as the project's selector form;
- a memoized selector wraps something cheap, with no real memoization gain;
- several updates are dispatched one after another where the layer supports one batched update;
- callbacks are threaded down from parents when the child could trigger the update itself;
- reducers or stores do more than update state (persistence, network or storage writes belong in the side-effect
  layer or a separate file);
- action creators reach into another module's state records;
- side-effect handlers skip the layer's own concurrency and call helpers, or exist only to forward one action that a
  direct update would do;
- the same data is kept in two places (component state copying the store, a cache copying a selector).

**Counter-example**
- A component-local value that nothing else reads belongs in local state, not the shared store.
