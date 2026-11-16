---
seen:
label: Security
quick: true
---
# Security and access

Everything the client sends is untrusted until checked on the server.

**Finding when:**
- a client-supplied id or hash is used without the project's ownership-and-role check (find the getter siblings use),
  and the query does not include the user or account id either;
- sequential numeric ids are exposed to the client where the project uses opaque ids or hashes;
- feature or plan access is checked only in the UI and not on the server, on read and on write;
- decoded external input is used without validation (types and required fields checked, throw on mismatch; parsing
  wrapped so malformed input fails cleanly);
- access rights are wider than needed (making a deliberately private file or bucket public);
- secrets or internal URLs end up in a client bundle;
- a scheduled job or server entry point has no health check;
- an admin action is not written to an audit log.

**Not a finding:**
- input validated once at the boundary and trusted afterwards inside the server.
