---
seen:
label: Design system
quick: true
---
# Project building blocks

UI uses the component library, theme and tokens the project already has, not a workaround around them. Before
judging, learn the project's own building blocks: read `package.json` (which component and styling libraries are
installed), `AGENTS.md` / `CLAUDE.md` (and any design-system docs they point to), and the closest sibling component.
Judge against what you found. If the project has no component library or theme, only the theme-value bullets apply.

**Finding when:**
- styling skips the preferred order: the component's theme definition first, then its own props, then composition
  with layout primitives, and one-off inline style overrides last;
- size-dependent spacing is set per use instead of as a size variant in the theme;
- interaction states (hover, focus, disabled, selected) are styled by hand instead of with the library's state hooks
  or classes in the theme;
- a thin wrapper around a library component carries inline style overrides, or overrides what a wrapper prop already
  controls;
- values bypass the theme: raw spacing, colors or font sizes; a new color that duplicates an existing one or exists in
  only one of the light and dark themes;
- a shared component gains props without its preview/documentation entry (controls for new props, an entry for a new
  component, required props marked, enum options matching the values used); app-only components need none;
- the wrong layer gets the code: base wrappers hold only library props, shared patterns live in the shared layer,
  feature-specific components live in the app;
- an app-level wrapper reuses the name of a library component, or names drift from the library or design tool;
- the wrapper API is loose: enums wider than the values used today, defaults missing for optional props the library
  does not default, library defaults redeclared, always-passed props left optional, base prop types not extended,
  mutually exclusive props not modeled as a typed union;
- a theme edit changes every app that shares the theme without a note that design agreed;
- a new page is built on a legacy component set the project is migrating away from.

**Counter-example**
- Pages still on a legacy component set keep it until they are migrated.
- A truly local one-off may use an inline style override.
- Requests for per-component index files or runtime prop-type declarations are obsolete when the project uses types.
