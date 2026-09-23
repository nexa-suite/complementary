# Nexa Design Lab inventory

This is the v1.0.2 inventory snapshot. The canonical source remains the
repository, so re-run the source checks when the Design Lab tag changes:

```bash
cd /Users/diegosandoval284/Developer/nexa-suite/design-lab
rg --files projects/nexa-ui/src/lib | sort
rg -o "path: '[^']+'" src/app/documentation/navigation/documentation-registry.ts
```

The released Lab currently exposes 57 registered documentation pages, 12
public reusable Angular candidates, 20 component documentation pages, 16
pattern pages, 8 foundation pages, 5 quality pages, and 5 engineering pages.

## Public reusable candidates and complete option surface

These are the current public exports from
`projects/nexa-ui/src/public-api.ts`. Do not infer a public component from a
documentation page alone.

| Candidate | Selector | Options / model / events |
| --- | --- | --- |
| Action Menu | `nexa-action-menu` | required `triggerId`, `triggerLabel`, `menuLabel`, `items`; `size`: `default \| compact`; item fields: `id`, `label`, optional `icon`, `shortcut`, `disabled`, `destructive`, `separatorBefore`; emits selected id. |
| Logo | `nexa-logo` | `variant`: `primary \| inverse`; `alt`; `decorative`. Uses supplied canonical assets. |
| Button | `nexa-button` | `variant`: `primary \| secondary \| quiet \| danger`; `size`: `compact \| standard \| large`; `type`: `button \| submit \| reset`; `disabled`, `loading`, `fullWidth`, optional `routerLink`, optional `ariaLabel`. |
| Numeric Stepper | `nexa-numeric-stepper` | required `id`, `label`; model `value`; `min`, `max`, `step`, `disabled`; clamps increment/decrement to bounds. |
| Range Slider | `nexa-range-slider` | required `id`, `label`; model `value`; `min`, `max`, `step`, `unit`, `disabled`; always exposes the current value. |
| Locale Switcher | `nexa-locale-switcher` | `label`; model `locale`: `en \| es`; uses the shared Segmented Control language. |
| Segmented Control | `nexa-segmented-control` | required `label`, `options`, model `selected`; `size`: `compact \| standard`; option fields `value`, `label`, optional `disabled`. |
| Status Chip | `nexa-status-chip` | `tone`: `success \| info \| warning \| danger \| neutral`; `emphasis`: `subtle \| standard \| strong`. |
| Surface | `nexa-surface` | `tone`: `default \| soft \| inset`; composition only, not a universal Box abstraction. |
| Text Field | `nexa-text-field` | required `id`, `label`; model `value`; `type`: `text \| search \| email \| password`; `placeholder`, `helper`, `error`, `required`, `disabled`, `readOnly`, `leadingIcon`, `trailingActionLabel`; emits trailing action and touch; implements `FormValueControl<string>`. |
| Toggle | `nexa-toggle` | required `id`, `label`; model `checked`; `disabled`; emits touch; implements `FormCheckboxControl`. |
| Tooltip | `nexa-tooltip` | required `id`, `content`, `triggerLabel`; focus/hover trigger, Escape dismissal, viewport-safe placement: `below`, `above`, `start`, `end`. |

The public export count is intentionally explicit. Documentation, State
Sequence, contrast parsing, evaluation modes, screenshot evidence, and route
frames are not part of this table or the package API.

## Full documentation route inventory

### Start here — 3

- `guidelines/overview`
- `guidelines/principles`
- `guidelines/maturity`

### Foundations — 8

- `guidelines/foundations/color`
- `guidelines/foundations/brand-logo`
- `guidelines/foundations/typography`
- `guidelines/foundations/layout-spacing`
- `guidelines/foundations/shape-radius`
- `guidelines/foundations/surfaces`
- `guidelines/foundations/iconography`
- `guidelines/foundations/motion`

### Components — 20

- `guidelines/components/buttons`
- `guidelines/components/text-fields`
- `guidelines/components/search-fields`
- `guidelines/components/select-combobox`
- `guidelines/components/checkbox`
- `guidelines/components/radio`
- `guidelines/components/toggle`
- `guidelines/components/segmented-control`
- `guidelines/components/status-badges`
- `guidelines/components/alerts-feedback`
- `guidelines/components/menus`
- `guidelines/components/tooltips`
- `guidelines/components/dialogs-overlays`
- `guidelines/components/cards-surfaces`
- `guidelines/components/lists-tables`
- `guidelines/components/progress-indicators`
- `guidelines/components/workflow-steps`
- `guidelines/components/numeric-stepper`
- `guidelines/components/slider`
- `guidelines/components/navigation-sidebars`

### Patterns — 16

- `guidelines/patterns/forms`
- `guidelines/patterns/search-filtering`
- `guidelines/patterns/async-operations`
- `guidelines/patterns/empty-loading-error`
- `guidelines/patterns/authentication`
- `guidelines/patterns/legal-content`
- `guidelines/patterns/payments`
- `guidelines/patterns/analytics`
- `guidelines/patterns/dispatch-board`
- `guidelines/patterns/data-dense-operations`
- `guidelines/patterns/responsive`
- `guidelines/patterns/catalog`
- `guidelines/patterns/request-builder`
- `guidelines/patterns/order-flow`
- `guidelines/patterns/delivery-pod`
- `guidelines/patterns/map-location`

### Quality — 5

- `guidelines/quality/accessibility-lab`
- `guidelines/quality/contrast-lab`
- `guidelines/quality/heuristics`
- `guidelines/quality/input-modality`
- `guidelines/quality/component-maturity`

### Engineering — 5

- `guidelines/engineering/angular-architecture`
- `guidelines/engineering/design-tokens`
- `guidelines/engineering/component-apis`
- `guidelines/engineering/testing`
- `guidelines/engineering/design-adoption`

The legacy aliases in `src/app/app.routes.ts` are redirects only: materials,
selection, overlays, progress-steppers, states, accessibility,
angular-compatibility, component-coverage, and figma-mapping. They do not add
new documentation pages.

## Explicitly absent from the current v1.0.2 surface

Completeness means complete coverage of the released Design Lab, not pretending
that every possible HTML control already has a Nexa contract. The current
release has no dedicated public candidate or documentation page for Textarea,
date/time inputs, file upload, pagination, accordion, autocomplete,
multiselect, or calendar. Payment evidence uses a local tablist for state
comparison; it is not a public Tabs component. If one of these is requested,
start with a documented native pattern and a product decision, then add the
new route/API/state contract to this inventory instead of silently inventing a
component.

## Component page behavior matrix

The 20 component pages cover these options and states:

| Page | Required evidence |
| --- | --- |
| Buttons | primary/secondary/quiet/danger intent; compact/standard/large; icon; full width; rest, hover, focus, pressed, disabled, processing, success, error; guarded link behavior. |
| Text Fields | text/search/email/password; empty, filled, focus, invalid, read-only, disabled, loading; helper/error association; leading/trailing actions. |
| Search Fields | query, clear, scope, searching, results, empty, error, retry; live status and preserved query. |
| Select & Combobox | native select, composite combobox, Action Menu comparison; closed/open/highlighted/selected/disabled/no-match; keyboard model. |
| Checkbox | unchecked, checked, indeterminate, hover, focus, disabled; native label and input. |
| Radio | fieldset/legend, unselected, selected, hover, focus, disabled; same-name group. |
| Toggle | on, off, hover, focus, disabled; immediate switch semantics, not deferred submit. |
| Segmented Control | small related options; selected, hover, focus, disabled option, compact/standard; immediate model update and `aria-pressed`. |
| Status & Badges | workflow, availability, priority, temperature families; icon + label + shape + tone; tone never color-only. |
| Alerts & Feedback | success, info, warning, error, recoverable retry/correction, urgency/persistence/dismissal. |
| Menus & Action Menus | open, command selection, disabled/destructive separation, Escape, arrows, Home/End, Enter/Space, Tab, outside click and focus restore. |
| Tooltips | visible supplement, hover/focus, placement, delay/dismissal, viewport edge behavior, `aria-describedby`; never critical meaning alone. |
| Dialogs & Overlays | open, close, Escape, scrim, focus, labelled title, modal semantics, recovery actions. |
| Cards & Surfaces | object card vs grouped panel vs plane; border, padding, radius, elevation, selected state; no universal Box. |
| Lists & Tables | semantic table, scoped headers, density, search/filter/sort, row status/action, empty, error and local horizontal overflow. |
| Progress Indicators | linear/circular determinate and indeterminate, inline activity, steps, paused, complete, error, content skeleton, reduced-motion fallback. |
| Workflow Steps | multi-phase current/complete/upcoming states; not a Numeric Stepper; accessible list and phase navigation. |
| Numeric Stepper | exact value, min/max/step boundaries, increment/decrement, disabled and labelled controls. |
| Slider | min/max/step, unit, min/middle/max, focus, disabled, visible output; pair with exact-value control when needed. |
| Navigation & Sidebars | frozen grouped sidebar, search, active row, disclosure, badge, router current state, focus restoration, mobile drawer and responsive geometry. |

## Tables, data, and chart fallback coverage

Do not omit data-display behavior when a screen is called a dashboard or
operations view:

- `lists-tables`: semantic table, scoped headers, local sort/filter/search,
  status composition, row action, empty/error state, and local horizontal
  scroll when the table cannot be meaningfully collapsed.
- `data-dense-operations`: rows, loading, error, empty, identifiers,
  operational status, compact density, and responsive local table behavior.
- `analytics`: every visualization answers a named question and has a text
  summary plus accessible details/table fallback; cover KPI/metric, progress
  ring, circular/donut composition, horizontal/grouped/stacked bars, line/area
  trend, sparkline, bullet/target, timeline/activity, status distribution,
  no-data, loading, and error only where useful.
- `catalog`: product identity, category/status, quantity/availability and
  selection/detail states; never imply inventory reservation from a card.

## Canonical state and viewport matrix

The browser contract covers every registered page plus these canonical route
matrices:

- Overview: default/focus.
- Color: default/semantic.
- Motion: standard/reduced.
- Buttons: default/hover/focus/pressed/disabled/loading/success/error.
- Progress: determinate/indeterminate/paused/complete/error/skeleton.
- Forms: idle/submitting/success/error/conflict.
- Async: error-terminal/cancelled-terminal.
- Empty/loading/error: first-use/no-results/filtered/loading/progress/partial/
  unavailable/permission/conflict/warning/error/non-retryable/success/
  cancelled/read-only/disabled.
- Authentication: default/focus/invalid/authenticating/credentials/workspace/
  success.
- Analytics: ready/loading/empty/error.
- Search: query/searching/results/empty/error.
- Payments: none/processing/saved/invalid/declined/unavailable.
- Request Builder: editable/quantity/submitted.
- Order Flow: submitted/validated/confirmed/documents.
- Delivery/POD: pending/received.
- Map/Location: ready/no-geolocation/provider-unavailable/address-fallback.
- Dispatch Board: empty/selected/source/destination/completed/warning/critical/
  blocked.
- Catalog: default/selected/detail.
- Responsive: desktop/tablet/mobile/reflow.
- Accessibility Lab: focus/contrast/text-200/text-spacing/reflow-400/
  reduced-motion.
- Component APIs: inventory/boundary.

Required layout widths are 1440, 1024, 768, 390, and 320px. High-risk pages
also require 200% text and 400% reflow review. This matrix is evidence coverage;
it does not certify the production application or assistive-technology support.
