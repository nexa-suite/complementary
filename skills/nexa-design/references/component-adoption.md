# Component adoption and Angular boundaries

`projects/nexa-ui` is the reusable Angular candidate boundary. Its public
entrypoint is `projects/nexa-ui/src/public-api.ts`; consumers import from
`nexa-ui`, never from `projects/nexa-ui/src/lib`.

For the exhaustive v1.0.2 route, candidate, option, table, and state catalog,
see [inventory.md](inventory.md). This file explains the adoption decision;
the inventory records the current surface so it can be checked against source.

For implementation-ready Angular templates, bindings, native alternatives, and
presentation-layer checklists, read
[presentation-adoption.md](presentation-adoption.md).

## Reusable candidates

The current explicit public candidates are:

- `NexaButton`
- `NexaTextField`
- `NexaActionMenu`
- `NexaSegmentedControl`
- `NexaLocaleSwitcher`
- `NexaStatusChip`
- `NexaToggle`
- `NexaTooltip`
- `NexaLogo`
- `NexaNumericStepper`
- `NexaRangeSlider`
- `NexaSurface`

Each candidate should keep its `.ts`, template, styles, and spec together. It
must have a focused API, native semantics, token-backed geometry, and tests
for its actual behavior. Prefer Angular standalone components, strict template
checking, signal-first inputs/outputs, and the existing Angular forms/routing
conventions.

`NexaTextField` uses Angular's `FormValueControl<string>` and `NexaToggle`
uses `FormCheckboxControl`; consumers bind them with `[formField]` from
`@angular/forms/signals`. Do not introduce a parallel ControlValueAccessor
contract merely to make a specimen convenient.

## Adoption categories

Every documentation page should make its boundary explicit:

| Category | Meaning |
| --- | --- |
| `PUBLIC COMPONENT` | Exported reusable candidate with a focused contract and colocated tests. |
| `DOCUMENTED NATIVE PATTERN` | Native platform behavior documented for adoption; not a Nexa component API. |
| `COMPOSITION PATTERN` | Route-local product composition; it does not define domain contracts. |
| `LAB EVIDENCE ONLY` | Evaluation, foundation, engineering, or evidence infrastructure. |
| `DEFERRED / NOT PRODUCT READY` | Intentionally held back pending a product decision. |

Checkbox, Radio, and Progress are documented native patterns in the current
candidate. State Sequence, contrast utilities, evaluation modes, screenshot
contracts, and documentation frames are Lab-only. Do not export them through
`nexa-ui` or present them as production APIs.

## Where code belongs

```text
Design Lab / application
  src/app/shell/             route shell and navigation
  src/app/documentation/    focused page features and content
  src/app/lab/               evaluation, evidence and quality infrastructure

Reusable candidate package
  projects/nexa-ui/src/lib/  controls, brand primitives, colocated specs
  projects/nexa-ui/src/public-api.ts
```

Documentation registry metadata owns discovery/navigation only. Substantial
page copy, rationale, rendering contracts, and behavior belong with the page
feature. Do not recreate a mega-registry or a catch-all renderer.

## Decision sequence

Before creating a component:

1. Search the Design Lab public API and route registry.
2. Find the closest current candidate or native pattern.
3. Decide whether the requested behavior is reusable or route-local.
4. Preserve the existing tokens, semantics, state taxonomy, and geometry.
5. Add a colocated test for the behavior and expose it only if the public
   contract is intentional.

If an application needs a candidate, consume the package contract and tokens;
do not copy the Lab implementation into the application. If the behavior is
product-specific, keep the composition in the application and do not expand
`nexa-ui` solely to avoid local composition code.
