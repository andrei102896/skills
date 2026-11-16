---
seen:
label: Wrong comment
quick: true
---
# Comment the why

The default is no comment. A comment earns its place only when it carries what the code cannot: a reason, a
constraint, or the outside origin of a value.

**Finding when an added or changed comment:**
- restates the code, including doc-comment parameter and return tags that only repeat the signature;
- narrates the change or the refactor ("moved from X", "now uses Y", "fix for the earlier bug");
- contradicts the code next to it (also ask where the number or value in it came from);
- is stale: the code it describes changed in this diff and the comment did not;
- covers a bad name: a comment on a variable or function that a rename would make unnecessary;
- sits on a variable whose value has no outside origin (variables almost never need one);
- sits on a function and says neither why it exists nor shows a sample input and output.

A diff that adds many comments while none of its values is actually unclear is itself one finding.

**Not a finding:**
- doc-comment descriptions, usage examples, deprecation notes, and parameter notes that add units or a valid range;
- a comment on a value that comes from outside the code (a spec, a vendor limit, a measured number).

**Counter-example**
- A missing comment is a finding only when the why truly cannot be read from the code or its names.
