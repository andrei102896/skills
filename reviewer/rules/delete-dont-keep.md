---
seen:
label: Unused
quick: false
---
# Delete, don't keep

Code with no consumer today is removed in the same change, not kept for later.

**Finding when the diff adds or leaves behind:**
- unused functions, exports, props, params, fields or events (props left from an old design included);
- commented-out code blocks;
- stale docs describing behavior the diff removed;
- duplicate assets, unread theme or config keys, style classes nothing renders;
- debug console output;
- a removed feature's sibling files and assets, including stored objects in every environment;
- a helper whose last caller this diff removed.

**How to phrase it:**
- Public API surface that cannot be removed in one deploy: stop reading it now, mark it deprecated, remove it in the
  next release. The finding is a missing deprecation step, not "delete now".
- A change that masks the real bug instead of fixing it: fine to ship, but the finding says so and asks for a
  follow-up task for the cause.

**Counter-example**
- Code that has a caller outside the diff (search the repo before claiming "unused").
