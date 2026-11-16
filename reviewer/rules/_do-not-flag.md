---
seen:
label:
quick: false
---
# Do not flag

Binding noise filter: drop a candidate that matches any entry below.

- Formatting, import order and quote style: the formatter and linter own them. Exception, style as a symptom: a
  missing trailing comma the formatter would add (the local linter is not running), a variable introduced only to
  dodge line length, string concatenation and template strings mixed on one line.
- Test coverage on schema or model definition files.
- An untyped catch variable in existing code.
- Praise, summaries, restating the diff.
- Suggesting a new dependency where a few lines suffice. The reverse, replacing custom code with an established
  package the project already uses or should, is fair.
- Hypothetical future requirements; ask "is this needed now?" instead.
- Anything already raised on the PR by a bot or a person, including the same point re-posted under another name.
- Whitespace-only edits to docs whose change triggers a pipeline or job of their own.

## Tone

Direct. Phrased as a question when uncertain. Concrete evidence every time: the path, the existing helper, the
contradicting line. Never "consider refactoring".

Escalate, don't redesign: an architectural problem gets "this needs a discussion" plus what is wrong. Never prescribe
the fix, not even one line.
