---
seen:
label: Convention
quick: false
---
# Migrations

Schema changes must be reversible, non-blocking and shipped ahead of the code that needs them.

**Finding when:**
- a migration has no down/rollback step (no exemption for "unused" tables);
- a table alteration uses a form that locks the table when the database offers an online, non-locking form;
- a new table has no primary key;
- column order ignores the project's convention seen in sibling migrations (for example timestamp columns last);
- a foreign key on a statistics, history or log table cascades deletes;
- generated SQL is built by string concatenation of values;
- the same change ships migrations and application code together: the schema has to land and be applied first, in its
  own PR.

**Counter-example**
- None: the down step has no exemption.
