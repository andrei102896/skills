---
seen:
label: Misplaced
quick: false
---
# Logic at the right level

Flag logic that lands where it does not belong.

**Finding when:**
- a shared component learns a concept that belongs to a single caller;
- compensating logic exists only because something is mounted or called at the wrong level;
- the same branch is decided at two levels (parent and child both check it);
- a helper both performs an action and decides whether it should be performed;
- a fix lands in module A for a cause that lives in module B.

**How to phrase it:** as an escalation. Say what is wrong, where the decision belongs, and that it needs a
discussion. Do not invent a refactor unless the move is one or two lines.

**Counter-example**
- A prop that parameterizes behavior the component already owns is correct: a generic component with props is the
  goal. The smell is a foreign concept, not a new prop.
