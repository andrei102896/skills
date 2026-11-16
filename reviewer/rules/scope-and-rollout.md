---
seen:
label: Rollout
quick: false
---
# Scope and rollout

The change ships safely and stays inside its task.

**Finding when:**
- migrations ship in the same PR as application code (they go in their own PR, first);
- a fix grows far beyond its bug: the extra goes in a TODO and a separate PR;
- a shared component is widened casually: prefer the narrow change plus a TODO;
- a manual operations step (env var, bucket, queue, cron) is needed and the PR description does not say so;
- a shared component changes, or a line on a shared path is removed: ask for testing across the named callers;
- a function gains a parameter or a fallback: check the other callers; not passing it keeps the old behavior, so ask
  whether that is intended;
- every caller would repeat the same fallback: it belongs inside the function;
- the diff includes work that belongs to another task;
- a new feature flag is not registered everywhere the flag list is enumerated;
- dependency or runtime engine versions disagree across packages.

**Counter-example**
- A small adjacent fix the task cannot work without.
