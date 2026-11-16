---
seen:
label: Too broad
quick: false
---
# Pass only what's needed

Props, parameters, queries and payloads carry only what the receiver uses.

**Finding when:**
- a component or function receives a whole object and reads one or two fields;
- a database query selects every column, or loads a full row, to read one column;
- a whole environment, request or event object is forwarded where one value is used;
- a source value is passed so the receiver can derive what the caller could pass directly;
- memoization depends on a whole large array when a count or an id suffices.

**Counter-example**
- Passing the whole domain object is fine when the receiver genuinely uses most of it, or is the domain's own
  component.
