# Nexa presentation adoption

Read this reference before implementing or changing an Angular presentation
layer. It maps the released `nexa-ui` contract to real page composition. It is
the operational companion to [component-adoption.md](component-adoption.md)
and the exhaustive surface list in [inventory.md](inventory.md).

## Source of truth

The current Design Lab baseline is `v1.0.2`, source SHA
`87a84053d6d9a3301ce1fae4ed06059b97c55491`, at:

```text
/Users/diegosandoval284/Developer/nexa-suite/design-lab
```

The reusable Angular boundary is `projects/nexa-ui`. Consumers import only
from its package entrypoint:

```ts
import {
  NexaButton,
  NexaTextField,
  NexaSurface,
  NexaStatusChip,
} from 'nexa-ui';
import type { NexaActionMenuItem, NexaSegmentOption } from 'nexa-ui';
```

Never deep-import `projects/nexa-ui/src/lib/...`, copy a Lab implementation,
or infer a production API from a documentation route.

## Complete public candidate map

The package exports exactly these 12 candidates. The “use it for” column is a
presentation decision; the “do not” column prevents accidental expansion of
the public API.

| Candidate | Use it for | Required wiring and contract | Do not |
| --- | --- | --- | --- |
| `NexaButton` | Primary, secondary, quiet, and danger actions; submit/reset actions; guarded links. | `variant`: `primary \| secondary \| quiet \| danger`; `size`: `compact \| standard \| large`; `type`; `disabled`, `loading`, `fullWidth`; optional `routerLink`, `ariaLabel`. | Use a styled `div`, hide a disabled link with ARIA only, or make every action primary. |
| `NexaTextField` | Text, search, email, and password entry. | Required `id` and `label`; `value`; `type`; optional placeholder/helper/error/required/disabled/readOnly/leading icon/trailing action. Implements `FormValueControl<string>`. | Use placeholder as the label, concatenate validation into arbitrary markup, or create a local input skin. |
| `NexaActionMenu` | A command menu opened from a trigger. | Required `triggerId`, `triggerLabel`, `menuLabel`, `items`; `size`; items may have `icon`, `shortcut`, `disabled`, `destructive`, `separatorBefore`; listen to `selected`. | Use it as a form select, hide commands behind icons, or reimplement arrow/Escape/focus behavior. |
| `NexaSegmentedControl` | A small set of mutually exclusive view/filter choices. | Required `label`, `options`, `selected`; `size`; options have `value`, `label`, optional `disabled`; two-way model via `selected`/`selectedChange`. | Put unrelated navigation in one group or simulate selection with CSS only. |
| `NexaLocaleSwitcher` | The shared EN/ES locale choice. | Optional `label`; two-way `locale` model with `en \| es`. | Create a different locale selector for each pattern or pretend it provides production i18n. |
| `NexaStatusChip` | Compact workflow, availability, priority, and operational status. | `tone`: `success \| info \| warning \| danger \| neutral`; `emphasis`: `subtle \| standard \| strong`; pair with text. | Encode meaning by color alone, overload it with paragraphs, or equate every domain status with a tone. |
| `NexaSurface` | A semantic grouped plane with controlled surface treatment. | `tone`: `default \| soft \| inset`; compose content inside it. | Treat it as a universal `Box`, nest it for decoration, or use it to hide a layout model. |
| `NexaLogo` | Canonical Nexa brand plane. | `variant`: `primary \| inverse`; meaningful `alt` or `decorative`. | Redraw the wordmark, replace it with text, or use the inverse variant on the wrong surface. |
| `NexaToggle` | Immediate boolean setting or preference. | Required `id` and `label`; `checked`; `disabled`; implements `FormCheckboxControl`; use `[formField]` for signal forms. | Use it for submit-later confirmation, permission claims, or a multi-choice group. |
| `NexaNumericStepper` | Exact bounded integer quantity. | Required `id`, `label`; `value`; `min`, `max`, `step`, `disabled`; visible value and bounded increment/decrement. | Use it for workflow phases, hide bounds, or let API limits exist only in CSS. |
| `NexaRangeSlider` | Continuous or stepped value where relative adjustment is useful. | Required `id`, `label`; `value`; `min`, `max`, `step`, `unit`, `disabled`; visible current output. | Use it as the only way to enter an exact business value when precision matters. |
| `NexaTooltip` | Short supplementary explanation available on hover and focus. | Required `id`, `content`, `triggerLabel`; optional projected trigger content; focus/hover and Escape behavior; placements are `below`, `above`, `start`, `end`. | Put critical instructions only in a tooltip, use it as a popover/menu, or attach it to an unlabeled icon. |

## Angular usage recipes

Examples below show the contract, not a copy-paste page. Keep state in the
feature that owns the route and use the host application's existing signal,
forms, routing, and data conventions.

### Actions and navigation

```html
<nexa-button
  type="submit"
  variant="primary"
  size="standard"
  [loading]="saving()"
  [disabled]="formInvalid() || saving()"
>
  Save request
</nexa-button>

<nexa-button
  variant="secondary"
  [routerLink]="['/sales/requests', requestId()]"
  [loading]="opening()"
>
  View request
</nexa-button>
```

`loading` is an interaction state, not decoration. A loading or disabled
router link must not navigate by pointer or keyboard. Use `type="button"` for
non-submit actions inside a form.

```ts
readonly menuItems: readonly NexaActionMenuItem[] = [
  { id: 'export', label: 'Export request', icon: 'pi-download', shortcut: '⌘E' },
  { id: 'archive', label: 'Archive', destructive: true, separatorBefore: true },
];

protected onMenuSelection(id: string): void {
  if (id === 'export') this.exportRequest();
  if (id === 'archive') this.archiveRequest();
}
```

```html
<nexa-action-menu
  triggerId="request-actions"
  triggerLabel="Request actions"
  menuLabel="Request actions"
  [items]="menuItems"
  (selected)="onMenuSelection($event)"
>
  <span trigger>Actions</span>
</nexa-action-menu>
```

Action Menu already owns the command-menu keyboard path: Enter/Space,
ArrowUp/ArrowDown, Home/End, Escape, outside click, disabled items, and focus
restoration. Do not add a second document listener in the page.

### Text entry and signal forms

For a local model, the component's `value` model is sufficient:

```html
<nexa-text-field
  id="buyer-search"
  label="Search buyers"
  type="search"
  placeholder="Name or account"
  [value]="query()"
  (valueChange)="query.set($event)"
  helper="Search by buyer name or account code."
  [error]="queryError()"
  trailingActionLabel="Clear search"
  (trailingAction)="query.set('')"
/>
```

`NexaTextField` associates its label, helper, error, invalid state, and
trailing action. Keep error text tied to actual validation or API state; do not
render an error merely because a specimen needs more content.

The component implements Angular's `FormValueControl<string>`. In an
application using signal forms, bind it through the form-field directive and
keep validation in the form model:

```html
<nexa-text-field id="email" label="Email" type="email" [formField]="login.email" />
```

`NexaToggle` follows the same rule through `FormCheckboxControl`:

```html
<nexa-toggle id="remember" label="Remember this device" [formField]="login.remember" />
```

For checkbox, radio, select, textarea, date/time, file, and other controls
without a public Nexa candidate, use the native element plus Nexa tokens and
semantic form structure. Do not invent a `NexaCheckbox` or `NexaSelect`.

### Selection and locale

Use `NexaSegmentedControl` only for a small related set. Keep the model
immediate so the selected visual responds in the same activation path:

```ts
readonly view = signal<'orders' | 'documents' | 'buyers'>('orders');
readonly viewOptions: readonly NexaSegmentOption[] = [
  { value: 'orders', label: 'Orders' },
  { value: 'documents', label: 'Documents' },
  { value: 'buyers', label: 'Buyers' },
];
```

```html
<nexa-segmented-control
  label="Operations view"
  [options]="viewOptions"
  [selected]="view()"
  (selectedChange)="view.set($event as 'orders' | 'documents' | 'buyers')"
/>
```

For EN/ES evidence or a product composition that needs the established
language control, use one `NexaLocaleSwitcher` composition:

```html
<nexa-locale-switcher label="Language" [(locale)]="locale" />
```

The switcher demonstrates local selection only. It is not a production
translation provider or an i18n architecture decision.

### Values, status, surfaces, brand, and help

```html
<nexa-numeric-stepper
  id="quantity"
  label="Quantity"
  [value]="quantity()"
  (valueChange)="quantity.set($event)"
  [min]="1"
  [max]="available()"
  [step]="1"
/>

<nexa-range-slider
  id="temperature"
  label="Temperature threshold"
  [value]="threshold()"
  (valueChange)="threshold.set($event)"
  [min]="-20"
  [max]="10"
  [step]="1"
  unit="°C"
/>
```

Always expose quantity bounds and the slider's current value. If an exact
value is business-critical, pair the slider with an exact field or stepper.

```html
<nexa-surface tone="soft">
  <header>
    <h2>Purchase request</h2>
    <nexa-status-chip tone="warning" emphasis="standard">Needs review</nexa-status-chip>
  </header>
  <!-- semantic page content -->
</nexa-surface>

<nexa-logo variant="primary" alt="Nexa" />

<nexa-tooltip id="credit-help" content="Credit is checked against the buyer account." triggerLabel="Credit help">
  <i class="pi pi-info-circle" aria-hidden="true"></i>
</nexa-tooltip>
```

Use an accessible name on tooltip triggers, keep the message brief, and put
critical information in the page content as well.

## Public component versus native pattern

Use this decision table before creating markup:

| Need | Decision |
| --- | --- |
| Action or navigation | `NexaButton`; use a real link when the action is navigation and does not need the candidate's guarded loading behavior. |
| Text/search/email/password | `NexaTextField`. |
| Boolean preference | `NexaToggle`; native checkbox when the visual/domain contract is checkbox semantics. |
| Mutually exclusive small view set | `NexaSegmentedControl`; native radio group when the choice is a form answer. |
| EN/ES switch | `NexaLocaleSwitcher`. |
| Command list | `NexaActionMenu`; native `<select>` for a simple form value, not a command menu. |
| Single select/combobox | Native `<select>` unless a real combobox interaction is required and its keyboard/ARIA contract is implemented and tested. |
| Status | `NexaStatusChip` plus visible text; tone is not the domain model. |
| Grouped surface | `NexaSurface` only when a surface treatment communicates grouping. |
| Tooltip | `NexaTooltip` for supplementary, non-critical help. |
| Checkbox/radio/progress/table/dialog | Use native semantics and the documented pattern. These are not current public Nexa candidates. |
| Tabs, textarea, date/time, file upload, pagination, accordion, autocomplete, multiselect, calendar | No current public Nexa contract. Start with native semantics and a product decision; do not invent a selector. |

Required native structures include `label`/`for`, `fieldset`/`legend` for radio
groups, scoped table headers, real button/link elements, visible focus, and a
real dialog/overlay contract when modal behavior is needed. ARIA attributes do
not replace behavior.

## Presentation-layer implementation sequence

1. Inspect the target route, Blueprint vocabulary, existing API/permission
   contract, and the matching Design Lab page.
2. Classify each visible element as public candidate, documented native
   pattern, product composition, or Lab-only evidence.
3. Define route state with signals and real data. Keep loading, empty, error,
   retry, success, and cancellation explicit where the feature can reach them.
4. Import public candidates from `nexa-ui`; never copy their source or deep
   import implementation files.
5. Compose semantic HTML around the candidates. The application owns the page
   layout, domain labels, data fetching, permissions, and route transitions.
6. Use semantic Nexa tokens and existing layout conventions. Do not create a
   generic `Box`, local token system, arbitrary geometry, negative margins, or
   CSS that overrides component states.
7. Separate phase position from visual tone. “Visited” is not automatically
   green; domain “cancelled” is not automatically a danger tone.
8. Verify keyboard, pointer, touch target, focus, accessible name/role/state,
   reduced motion, increased contrast, and console cleanliness.
9. Test the feature at 1440, 1024, 768, 390, and 320px. Check 200% text and
   400% reflow on dense or state-heavy pages.
10. Keep component tests beside the component and application integration tests
    at the feature boundary. Run the proportional Design Lab and application
    gates before claiming completion.

## Presentation contract checklist

- [ ] Angular standalone feature with strict templates and the host app's
      signal/forms/routing conventions.
- [ ] Public candidates imported only from `nexa-ui`; no deep imports.
- [ ] No copied `src/app` documentation renderer or `projects/nexa-ui` source.
- [ ] Business vocabulary, API contracts, tenant scope, permissions, and
      recovery actions come from the application/Blueprint, not the Lab.
- [ ] Native elements carry native behavior; ARIA supplements rather than
      substitutes for keyboard, focus, disabled, or modal behavior.
- [ ] Labels, descriptions, errors, status updates, and table relationships
      are programmatically associated.
- [ ] Loading, empty, error, retry, success, and cancelled semantics are real
      and not filler sections copied from another page.
- [ ] Selected, hover, pressed, focus, loading, and overlay layers preserve
      the component's base radius and inset geometry.
- [ ] Color and icon communicate meaning; PrimeIcons remain the approved icon
      language and icons are not used as the only label.
- [ ] No Lab-only State Sequence, contrast utility, screenshot contract, or
      evaluation mode is promoted into a production component API.
- [ ] Feature tests cover the interaction path; visual evidence does not
      replace behavioral tests or human accessibility review.

## When something was not copied

If an implementation seems to be missing something from the Design Lab:

1. Check `public-api.ts`. If the candidate is not exported, it is not a
   production package contract.
2. Check `inventory.md` for the page's category. A component page may document
   a native pattern or a composition rather than export a component.
3. Compare the actual input/model/output names in the candidate contract.
   Documentation examples are not permission to rename or invent bindings.
4. Check whether the missing behavior belongs to the application: data,
   permissions, routing, API states, or domain recovery are not owned by the
   Design Lab.
5. If the gap is genuinely reusable, record a product/design decision and add
   the candidate, tests, public export, tokens, docs, and inventory entry as a
   separate change. Do not patch around it with a second unofficial component.

## Delivery and validation

For a presentation-layer change, report the Design Lab tag/SHA, changed
application feature files, public candidates consumed, native patterns used,
responsive evidence, behavioral tests, and any human review still pending.

For the Design Lab itself, run the gates in [validation.md](validation.md).
For the local skill, run the audit script and the skill validator. A passing
Design Lab audit does not prove a production application is integrated,
authorized, tenant-safe, or accessibility-certified.
