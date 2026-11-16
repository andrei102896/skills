---
seen:
label: Convention
quick: true
---
# Logging

Server code logs through the project's one shared logger. Find it first (search for the logger the sibling files
import) and cite it by name.

**Finding when:**
- server code writes to the console, wraps the logger per file, or installs its own ad-hoc error handler;
- the log call is not structured the way the shared logger expects (message, file, level, label, group or the
  project's equivalent fields);
- the message contains emoji, or repeats text already carried by the label or group fields;
- a failed outbound request is logged below error level;
- a catch block swallows an error without logging it;
- log-level plumbing is added somewhere other than next to the logger;
- console output is left in production code (an intentionally empty callback with a TODO is acceptable).

**Not a finding:**
- console output in scripts, tests or local tooling.

**Counter-example**
- A catch that rethrows, or converts the error into a returned failure the caller logs, needs no log of its own.
