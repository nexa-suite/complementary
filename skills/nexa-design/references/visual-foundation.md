# Nexa visual foundation

Use the released Design Lab (`v1.0.2`)
as the current visual baseline. Re-check the repository before relying on a
version number; the source is `/Users/diegosandoval284/Developer/nexa-suite/design-lab`.

## Frozen direction

- Canonical appearance is light. White structural surfaces sit on a cool,
  lightly tinted canvas; elevation is restrained and purposeful.
- The canonical Nexa logo comes from `logo-nexa/logo-nexa.svg` and
  `logo-nexa/Documento.svg`. Never redraw the wordmark with CSS or text.
- Preserve the sidebar/navigation geometry, grouping, search, active row,
  responsive drawer behavior, and text-field geometry.
- Candidate type hierarchy is Plus Jakarta Sans / Inter with JetBrains or
  system mono for code-like values. Do not introduce a novelty or retro font
  without a product decision.
- PrimeIcons are the approved icon system in the Lab. Use the local audited
  asset pipeline and meaningful icons; do not replace them with random icon
  libraries or text glyphs.
- Shape is semantic, not universal: control, card, panel, status, overlay,
  focus, and selected geometry can differ. Rounded does not mean every object
  is a pill or a high-radius AI card.

## Color, spacing, and density

The token model is:

```text
primitive -> semantic -> component / data visualization
```

Use semantic tokens in reusable and application UI. Generated SCSS under
`src/styles/_tokens-*.scss` and the generated token reference are outputs; edit
the JSON token sources, then regenerate and validate. Do not hard-code a
reusable color or arbitrary radius just to match one screenshot.

Use color to express state, hierarchy, and action. Avoid harsh gradients,
rainbow decoration, solid blocks that flatten the hierarchy, excessive pastel
surfaces, and `box-shadow` on every element. Keep the canvas, surfaces,
dividers, text contrast, focus ring, and semantic status roles legible before
adding visual personality.

Spacing must come from the established rhythm and focused aliases for control
padding, panel/card padding, gaps, interactive radius, and focus geometry.
Labels must not touch dividers. Selected layers, cards, and internal controls
must share the same inset and geometry model. Do not use negative margins to
mask a spacing defect.

## Anti-slop guardrails

Avoid generic AI landing-page or dashboard signals: decorative bento grids,
three-card feature rows, pricing tiers, fake testimonials, fake metrics,
terminal-window tropes, emoji UI, gratuitous tags, unexplained badges, em
dashes used as decoration, skeleton loaders as the default loading treatment,
and made-up product demos. These are not forbidden when a concrete product
requirement needs them, but they must not be added as filler.

Do not add gradients, unnecessary drop shadows, or a universal radius system.
Prefer a calm, operational, authentic Nexa composition with generous spacing,
clear hierarchy, and visible real states.

## Geometry and interaction integrity

- Base geometry governs hover, pressed, selected, focus, loading, and overlay
  layers. Internal pseudo-elements inherit the base radius where needed.
- Focus is visibly strong and remains inside the intended component geometry.
- Native semantics are preferred for links, buttons, inputs, checkbox/radio,
  and form controls. ARIA alone is not proof of disabled behavior.
- A disabled or loading link-style action must not navigate by pointer or
  keyboard.
- Action Menu and Tooltip presentation is frozen; only behavior may be refined
  when the change preserves keyboard, focus, outside-click, and placement
  quality.

## Current source references

When a decision is unclear, inspect these files in Design Lab:

- `README.md` for the released direction and boundary.
- `docs/architecture.md` for ownership and token laws.
- `docs/consuming-nexa-ui.md` for adoption categories.
- `src/styles/_tokens-*.scss` and `tokens/*.tokens.json` for current tokens.
- `src/app/shell/` for navigation geometry.
- `projects/nexa-ui/src/lib/` for reusable candidate implementations.
- `docs/archive/v0.x/` only for provenance, never as current authority.
