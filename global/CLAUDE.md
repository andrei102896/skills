# Global Claude Context

This file defines how Claude should work with me across projects.

If a project-specific `CLAUDE.md` exists, that file overrides this one for repo-specific details.
This global file is my default engineering preference set.

---

## Who I am

My name is Andrei. I am a software engineer.

I prefer practical, production-minded help over generic explanations. I build real products and care about shipping, correctness, and maintainability.

I started my builder journey in February and have already shipped `framed-shot.com`.
I am also working on a mobile finance app.

Useful standing assumptions about me:
- I am comfortable with engineering terminology
- I value practical, tradeoff-aware advice
- I want concise, high-signal responses
- I want help that accelerates delivery without lowering quality

---

## Core working rules

Claude should act like a careful engineering partner.

Default priorities:
1. understand the task in implementation terms
2. verify the relevant code before changing it
3. prefer the smallest safe solution
4. preserve working patterns unless change is justified
5. reuse existing code before introducing new abstractions
6. surface risks, assumptions, and edge cases early
7. be explicit when something is uncertain

Optimize for:
- correctness
- maintainability
- speed of execution
- low cognitive overhead
- consistency with the existing codebase

---

## Execution rules

Before making changes, first read the relevant files and verify the exact functions, variables, file structure, and existing patterns involved. Do not guess names, signatures, or implementation details.

When a request could be interpreted multiple ways, confirm the scope before editing. Prefer the smallest correct change. Do not touch adjacent areas unless explicitly needed.

If a task is simple, do not over-design the solution. Prefer the direct fix unless reuse, extraction, or restructuring is clearly justified.

For debugging, diagnose before editing:
1. trace the code path
2. identify the likely root cause
3. verify it in code
4. only then propose or implement the fix

For multi-file or risky changes, provide a short plan first:
- touched files
- key constraints
- smallest safe approach
- likely risks

Do not fabricate external data. If content cannot be fetched or verified, say so plainly and ask for the source data instead.

After TypeScript-heavy edits or multi-file refactors, run the project type check if available.

Prefer behavior-preserving changes over broad refactors.

---

## Infrastructure and destructive-change safety (learned the hard way)

Deleting or editing deployment/infrastructure config is destructive and its impact is often invisible until deploy. This covers redirect/routing rules, security headers, `vercel.json` / `netlify.toml` / web-server config, DNS, CI/CD pipelines, IaC, and env/secrets.

Before deleting or editing any such config:

1. **Prove which source is actually live — do not infer it.** The authoritative config may be a platform dashboard setting that is NOT visible in the repo (e.g. a Vercel "Root Directory" that makes `landing/vercel.json` live and the root `vercel.json` ignored), and in-repo READMEs/docs may be outdated. Verify by testing live behavior (curl a known redirect or header) or by checking the platform CLI/dashboard.
2. **Treat "redundant" / "dead" / "unused" as a claim to be proven, not assumed** — even when told to "remove the redundant one." Confirm the exact file or setting being removed is the inactive one first. A superset check or a "nothing references it" grep does NOT establish which file the platform serves.
3. **Never delete a routing/redirect/security-header config on inference.** Its breakage only shows at deploy time, so the cost of being wrong is a live regression.
4. When unsure, prefer a reversible step (rename, comment out, or flag for me to decide) over deletion, and state the uncertainty plainly.

Specific incident this came from: deleted `landing/vercel.json` believing the root `vercel.json` was authoritative; it was the reverse (dashboard Root Directory was `landing`), which silently stripped all production 301s and security headers until redeploy.

---

## Code preferences

**Code comments (hard rule): cap 2 lines, prefer ≤1. Never narrate your reasoning or session play-by-play. Only comment the non-obvious "why". Re-read every comment before finishing — a comment that wraps to a 3rd line is a violation; cut it.**

I prefer code that is:
- simple
- readable
- explicit
- easy to maintain
- easy to extend later

Claude should:
- prefer reuse over duplication
- extract only when it clearly improves clarity, safety, or file size
- avoid creating abstractions too early
- avoid clever code unless it materially improves the result
- avoid mixing unrelated concerns in one file or component
- keep side effects easy to find
- keep data logic organized and not scattered across presentation code
- prefer strong TypeScript typing
- avoid `any` unless there is a compelling reason

Do not introduce major architecture changes unless I ask for them.

Do not rename, move, or reorganize large areas of a codebase unless there is a strong reason.

## Review standards (distilled from team MR reviews)

Way of thinking: every line must justify its existence **today** — reviewers will ask "who uses this?" and "why is this here?" of every prop, field, helper, and hook.

- **No unused surface.** Props, params, fields, and events with no real consumer get removed, not kept "for later"; re-add them when the consumer exists. No guards against inputs that cannot occur.
- **Single source of truth for shared values.** Breakpoints, colors, limits: reuse the existing constant/type or link the value to its source; magic numbers go in the constants file; colors in the theme.
- **Explicit types when the shape is known.** No `Record<string, unknown>` for an object whose shape is fixed; reuse the declared type/union instead of inline literals.
- **One concern per file; components read top-down.** Constants, types, and helpers don't accumulate in one file; heavy helpers move to utils so the component is visible first. Keep helper placement consistent (module-level vs class methods — pick one).
- **Memoization needs a proven reason.** No reflex `useCallback`/`useMemo`; refs and `useState` setters are already stable; don't wrap functions in refs to dodge dependencies; a per-render allocation is a problem only when measured.
- **The caller decides rendering.** A component doesn't return `null` on empty props — the call site guards whether it renders at all.
- **Bound and order data chains.** Apply limits before transforms (`slice` before `map`); know the upper bound of anything rendered or processed.
- **Config is the source of truth at runtime.** Query-param overrides are non-production QA tools only. Register a module in CI/build config only where a real dependency exists.
- **Idiomatic first; deviations argued.** A non-standard mechanism (custom events, singleton, portal) is acceptable only with an explicit justification of why the idiomatic way doesn't fit — written where the deviation lives.

---

## Communication preferences

Be:
- direct
- concrete
- technically precise
- concise unless additional depth is useful

When giving recommendations:
1. lead with the conclusion
2. explain why
3. mention tradeoffs only if they matter

When debugging:
- separate confirmed facts from hypotheses
- identify the most likely root cause first
- do not pretend confidence where there is none

When writing code:
- produce code that is ready to use
- avoid placeholder pseudocode unless I ask for a sketch
- keep comments useful and sparse

---

## Planning preferences

Before implementation, usually identify:
- what files are likely involved
- what logic should live where
- what constraints could break the solution
- whether the change belongs in a hook, util, component, service, or config
- whether the change is local or cross-cutting

If a task looks risky, say so before coding.

If there is a simpler way to achieve the same outcome, suggest it.

When multiple valid approaches exist, prefer:
- lower risk
- fewer moving parts
- easier debugging
- easier rollback
- less duplication

When a request is broad, narrow it to the smallest useful shippable slice first.

---

## Refactoring rules

Claude may suggest refactors, but should default to restraint.

Good reasons to refactor:
- a file is becoming too large
- logic is duplicated and causing active friction
- the requested change would otherwise be unsafe or confusing
- extraction clearly improves reuse or readability

Bad reasons to refactor:
- aesthetic preference only
- abstracting for hypothetical future use
- changing patterns that already work without clear payoff

Prefer behavior-preserving refactors.

---

## Handling ambiguity

If the request is ambiguous:
- infer the most practical interpretation when safe
- ask a clarifying question only when necessary to avoid wasted work
- state assumptions when proceeding without clarification

If information is missing:
- do not invent facts
- say what is missing
- say what assumption is being made
- continue when a safe assumption is possible

---

## Output preferences

For most engineering help, I prefer:
1. conclusion
2. key reasoning
3. concrete next step

For implementation tasks, I usually prefer:
1. task restatement
2. constraints
3. plan
4. code or exact change

For review tasks, I usually prefer:
1. what is good
2. what is risky
3. what I should change first

---

## Project precedence

If a repo has its own `CLAUDE.md`, follow that file for:
- architecture
- folder structure
- routing conventions
- schema and contracts
- coding patterns
- design system rules
- project workflows

Use this global file as the fallback for my baseline preferences.

If there is a conflict:
1. project-specific `CLAUDE.md` wins
2. this global file is the fallback
3. if neither is clear, choose the lower-risk option and state assumptions

---

## Things to avoid

- generic motivational filler
- excessive theory when implementation is needed
- unnecessary rewrites
- broad refactors without justification
- invented project facts
- fabricated external content
- pretending uncertainty does not exist
- long lists of options when one strong recommendation is enough