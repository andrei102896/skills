---
seen:
label: Convention
quick: false
---
# API layer conventions

Judge changes to the project's own API layer (schema, resolvers, route handlers, RPC endpoints) against the way that
layer already works. Before judging, learn it: read `package.json`, `AGENTS.md` / `CLAUDE.md` and the closest sibling
endpoint to the changed one. Name the project's own auth guard, error wrapper and shared types when you cite them.
If the diff touches no API layer, this rule does not apply.

**Finding when:**
- the change breaks backward compatibility between deploys: an argument or field removed, renamed or made required
  while old clients still call it (deprecate first, remove in a later release);
- the declared return type does not match what the handler returns (including skipping the project's response
  wrapper when the declared type expects it);
- a required argument is declared optional or nullable (lists of required items included);
- the auth or permission check runs inside a try/catch that can swallow its rejection, or runs after work has started;
- errors are mapped to client responses in more than one place instead of once, the project's way;
- request or response types are written by hand when generated or shared types already exist for them;
- a constant or type is exported from an API file with no other importer.

**Counter-example**
- A new optional argument with a default that keeps old behavior is backward compatible.
