---
name: nexa-design
description: "Build, review, or refine Nexa Angular interfaces using the released Design Lab as the visual and component source of truth, with token, accessibility, responsive, and evidence-aware decisions."
---

# Nexa Design

Use this skill for Nexa Design Lab work and for frontend work that must consume
Nexa's visual foundation: Angular screens, reusable UI candidates, product
compositions, visual parity, interaction states, responsive behavior, and
design-system review.

## Source hierarchy and boundaries

1. Product decisions and the Blueprint define business vocabulary, contracts,
   architecture, and adoption decisions.
2. The released Design Lab at
   `/Users/diegosandoval284/Developer/nexa-suite/design-lab` (`v1.0.2`) and
   `https://github.com/nexa-suite/design-lab` define executable visual evidence,
   component candidates, tokens, interaction states, and validation contracts.
3. Vue/Legacy repositories and the local `FLOW/` reference assets are visual
   and flow evidence only. They do not authorize copying legacy architecture,
   inventing domain behavior, or bypassing the Blueprint.

Before changing a production application, verify the current Design Lab tag,
the target application's Git root and branch, and the relevant Blueprint
decision. Do not treat archived v0.x reports or old prompts as current visual
authority when the released Design Lab contradicts them.

Never modify Mobile, Legacy applications, production API contracts, Blueprint
governance, or `main` merely because a design task touches them. A visual
specimen is not a production workflow, domain rule, accessibility
certification, or provider integration.

## Required working method

- Inspect the existing route, component, tokens, tests, and Design Lab evidence
  before creating anything.
- Prefer KEEP → REFINE → REWORK. Make the smallest coherent increment that
  closes the requested behavior instead of adding a parallel design system.
- Decide whether the result is a reusable component, a documented native
  pattern, a product composition, or Lab-only evidence. Do not promote Lab
  infrastructure such as State Sequence or contrast utilities into a product
  API.
- Keep Angular files and tests together. Use standalone Angular components,
  strict templates, native semantics, signal-first state, and the repository's
  existing form/routing conventions.
- When implementing a presentation layer, read
  [presentation-adoption.md](references/presentation-adoption.md) before
  authoring templates. It maps every public candidate to its real contract,
  native alternatives, Angular wiring, and page-level validation.
- Preserve real domain and REST contracts. Do not invent endpoints, entities,
  statuses, maps providers, payment behavior, or seeded organizations to make
  a screen look complete.

Read the focused reference only when needed:

- [visual-foundation.md](references/visual-foundation.md) for identity,
  geometry, typography, color, icon, spacing, and anti-slop rules.
- [component-adoption.md](references/component-adoption.md) for reusable
  `nexa-ui` boundaries, adoption categories, and Angular usage.
- [inventory.md](references/inventory.md) for the complete v1.0.2 page,
  component, option, table, pattern, and state inventory.
- [flows-and-evidence.md](references/flows-and-evidence.md) for product-flow
  compositions, state semantics, FLOW references, and responsive behavior.
- [validation.md](references/validation.md) for deterministic Design Lab gates
  and evidence expectations.

When the Design Lab version changes or a new component is added, run
`node scripts/audit-design-lab.mjs --repo /Users/diegosandoval284/Developer/nexa-suite/design-lab`.
It mechanically checks registry/content parity, canonical evidence routes,
public exports, colocated implementation files, and signal API fields before
you update the inventory.

## UI decision rules

- Start from the current Design Lab component or pattern. Reuse its public
  contract and tokens before writing local CSS.
- Keep the light Nexa foundation, canonical logo assets, sidebar/navigation
  geometry, text-field geometry, type hierarchy, PrimeIcons, and keyboard
  interaction language consistent with the released baseline.
- Use semantic geometry: a control, card, panel, status, selected layer, and
  overlay may have different radii. Do not make every surface a pill or a
  generic rounded card. Selected, focus, pressed, loading, and overlay layers
  must inherit the base shape; no accidental square corners.
- Use color for meaning and hierarchy, not decoration. Avoid gradients,
  rainbow UI, fake metrics, fake testimonials, emojis, gratuitous shadows,
  decorative tags, and generic AI-dashboard/bento patterns unless a real
  product requirement and the Design Lab evidence justify them.
- Every meaningful interaction needs keyboard/focus behavior, a usable target,
  accessible name/role/state, and honest loading, empty, error, recovery, and
  success semantics. Reduced Motion and Increased Contrast must remain
  understandable.
- Preserve generous, systematic spacing. Fix the layout model or token rather
  than hiding defects with negative margins or arbitrary one-off geometry.

## Completion standard

Do not report a design task complete because a screenshot looks plausible. The
changed behavior must be wired, responsive, accessible, and validated at the
scope of the request. For a reusable candidate, prove public API boundaries,
native semantics, colocated tests, token usage, and package/build integrity.
For a product flow, prove the real API/permission/error path or explicitly
label the result as a composition specimen.

For visual work, validate at 1440, 1024, 768, 390, and 320px when applicable;
review 200% text and 400% reflow for high-risk surfaces; inspect console and
overflow behavior; and keep human visual and assistive-technology review
separate from automated evidence. Use the commands in
[validation.md](references/validation.md) proportionally to the change.

## SCM boundary

Use feature branches and conventional commits. Do not push directly to
`main`, rewrite history, move tags, or publish a release unless the user has
explicitly authorized that exact action. Keep the Design Lab isolated from
production application and Blueprint changes, and report the exact repository,
branch, SHA, validation, and remaining human review items.
