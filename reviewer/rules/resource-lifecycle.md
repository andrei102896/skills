---
seen:
label: Resource
quick: false
---
# Resource lifecycle

Resources are created once, reused, released, and bounded.

**Finding when:**
- a serverless handler creates its client per invocation instead of once outside the handler (return early if
  already connected);
- more than one client for the same object storage or service exists where one global client is the pattern;
- a large file is read into memory instead of streamed to disk;
- the same file is uploaded several times;
- object URLs are never revoked, or abandoned responses and streams are never destroyed;
- a queue's visibility or lease timeout is shorter than the longest job it guards;
- concurrent writers update a shared counter without an atomic operation;
- a retry loop counts in the wrong direction or has no upper bound;
- hot-path lookup tables, debounced functions or theme providers are recreated per render or per component;
- a recurring correctness trap appears: an empty object treated as false, a network call made with an empty list,
  `includes(x?.id)` that searches for undefined, parsing external text without handling a thrown error.

**Counter-example**
- A short-lived script or test that creates its client per run.
