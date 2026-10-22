---
name: project-init
description: Start a new project from zero to Andrei's standard — docs (AGENTS.md, README.md, PROGRESS.md, docs/ROADMAP.md), editor/format/lint/type configs, the Node pnpm-workspace toolchain for Node projects, git with the right identity — after its plan passes the two judges. Use when starting a new project or repo, or when asked to "init project", "init project docs", "new project", "create AGENTS.md" or "set up project rules".
---

# project-init

Sets up a new project the way "make it accessible" (MIA) is set up: the process (read order, hard rules, two judges, lessons, one `check` command) for every project, and MIA's Node-native toolchain for Node projects only.

## Workflow

1. **Discover.** Empty folder or existing repo (`git status`, `ls -A`). Infer name, purpose, type (Node CLI/backend/library, web app, browser extension, mobile), `node -v`, `pnpm -v`. Ask Andrei only what cannot be inferred (usually purpose and type). Never overwrite an existing file without showing what would change.

2. **Plan, judge, go.** Write the scaffold plan (files, type, toolchain, any deviation from this skill). Run the two judges on it per "Plans get two judges" in `~/.claude/CLAUDE.md`, then hand Andrei the revised plan with the findings table and wait for the go.

3. **Process layer (every type).**
   - Docs from `references/templates.md`: AGENTS.md (rules relevant to the stack from `references/common-rules.md`, copied in, the repo stays self-contained; under ~120 lines), README.md, PROGRESS.md, docs/ROADMAP.md.
   - From `assets/common/`: `editorconfig` → `.editorconfig`, `prettierrc.json` → `.prettierrc.json`, `prettierignore` → `.prettierignore`, `gitignore` → `.gitignore`.
   - No `.claude/agents` copies: the user-level judges serve every project. Add a project judge only when it must differ (MIA's design judge compares pages to PDFs).

4. **Toolchain.**
   - **Node CLI/backend/library** (MIA's layout: Node runs TypeScript natively, no build step):
     - From `assets/node/`: `package.json` (fill `{{NAME}}`, `{{PNPM_VERSION}}` from `pnpm -v`, `{{NODE_MAJOR}}`), `pnpm-workspace.yaml`, `tsconfig.base.json`, `eslint.config.js`. `.nvmrc` = the Node major.
     - Dev dependencies, exact pins, current versions (pnpm's release-age delay may hold back a version published days ago; that is expected):
       ```
       pnpm add -D -E -w eslint @eslint/js typescript-eslint eslint-config-prettier prettier @types/node@<node major>
       pnpm add -D -E -w "typescript@$(npm view typescript-eslint peerDependencies.typescript)"
       pnpm peers check
       ```
       The second line matters: the latest TypeScript can be ahead of typescript-eslint (TS 7 vs `<6.1.0` on 2026-10-22) and lint then crashes. `pnpm peers check` must report no issues.
     - No package is created: the first feature creates `packages/<name>/` with its first real module and test, following "New package" in AGENTS.md.
   - **Web app, browser extension, mobile:** the Node-native setup does not run in a browser (no build step). Ask Andrei for the toolchain (bundler, framework), then apply the same strictness to it: the `tsconfig.base.json` flags, the ESLint rules in `assets/node/eslint.config.js`, prettier, and a single `check` script.

5. **Validate.** `pnpm install` (or the chosen manager), then the `check` script. On a Node scaffold with no packages it passes with 0 packages and 0 tests: report it as vacuous, not as proof.

6. **Git hand-over.** Run `git init` only. Hand Andrei, in this order:
   ```
   git remote add origin git@github.com:andrei102896/<name>.git
   git add -A && git commit -m "Project setup" && git push -u origin main
   ```
   The remote must exist before the first commit: `~/.gitconfig` has `useConfigOnly` and picks the email by remote (`includeIf`), so a commit without a remote fails. Never commit or push yourself.

7. **Report.** Every file created, the validation output (with "vacuous" where it is), and what the first feature should create.

## Notes

- `references/common-rules.md` is the union of market-clean, nn-chrome-extension, tomapan and MIA, strictest wins. Promote a lesson there when it holds across projects (see the lessons rule in `~/.claude/CLAUDE.md`).
- Proving a lint rule works: put the probe inside a package with its own tsconfig and check the rule ID in the output (`max-lines`, `@typescript-eslint/consistent-type-assertions`); a file outside every tsconfig fails with a projectService parse error instead, which looks like a pass.
