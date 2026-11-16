---
seen:
label: Convention
quick: true
---
# Translation keys, not text

Data holds identifiers; text is produced at the render site.

**Finding when:**
- constant tables, presets, menus or API responses hold display text instead of translation keys;
- translation runs at module scope or inside constants (a global translate function) instead of at render time with
  the translation hook or function the component already has;
- a backend message that reaches the UI is a sentence instead of an identifier the client translates;
- an item keeps both a text field and a key field for the same thing;
- labels are reused as analytics event names without an explicit decision;
- the translation namespace order is inconsistent: the dominant namespace comes first and only the odd key names its
  own namespace.

**Not a finding:**
- developer-facing text: log messages, thrown internal errors, test names.

**Counter-example**
- Projects with no translation layer at all: skip this rule.
