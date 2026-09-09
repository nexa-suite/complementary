# Flows, compositions, and evidence

The Design Lab documents behavior and visual evidence. It does not define
production domain contracts. Use the current route feature and the local
`FLOW/` reference assets when present; the assets are evidence for sequence,
layout, and state, not an instruction to copy a legacy implementation.

## Product-flow grammar

When a product screen is requested, preserve the real business sequence and
label the result correctly:

```text
Buyer: login -> catalog -> SKU selection -> request builder -> purchase request
       -> sales order -> delivery visibility -> documents -> payments

Platform: administration -> customer management -> catalog -> sales
          -> warehouse -> fulfillment -> delivery -> finance
```

Do not collapse catalog browsing, cart, draft request, purchase request, and
sales order into one generic cart. A cart or draft must not imply inventory
reservation unless the API contract proves it.

Use existing routes before adding one. Current Design Lab evidence includes
catalog, request builder, order flow, delivery/proof, map/location,
authentication, payments, analytics, dispatch board, data-dense operations,
search/filtering, and responsive composition.

## State evidence

State evidence must demonstrate a meaningful behavior, not fill a template.

- Async operations stop at terminal states. Error remains terminal until
  Retry/recovery; success is terminal unless the specimen explicitly defines a
  next path; cancelled is terminal. Do not loop playback automatically.
- Model phase position separately from semantic tone. A phase can be future,
  current, or visited while independently being neutral, info, warning,
  danger, or success. Do not turn every visited phase green.
- Process Evidence belongs only on components with temporal behavior. Button,
  Search, Progress, and an explicit async composition may need it; Toggle and
  Radio do not need generic async evidence.
- Error, empty, loading, disabled, permission, conflict, read-only, warning,
  success, and cancelled are distinct states. Do not use a single spinner or
  skeleton to represent every state.
- Locale switching uses one reusable EN/ES composition based on the established
  Segmented Control language. Do not build separate selectors per pattern.

## Pattern-specific rules

- Authentication is a focused composition with the canonical Nexa brand plane.
  Demonstrate default, focus, invalid form, authenticating, invalid
  credentials, workspace detected, and success. Do not invent backend auth or
  anonymous organization registration.
- Analytics uses `question -> visualization -> text summary -> accessible
  data/details`. Every chart states the question it answers and has no-data,
  loading, error, and accessible fallback evidence where relevant. Prefer
  lightweight accessible SVG/CSS over a chart library unless the Lab genuinely
  needs one.
- Dispatch Board keeps its strong visual direction and demonstrates empty,
  selected, movement source/destination, completed, warning, critical, and
  blocked states. An accessible command path must remain equivalent to pointer
  movement. Reduced Motion must preserve meaning without spatial animation.
- Search demonstrates query, searching, results/empty/error, and retry.
- Progress demonstrates determinate/indeterminate linear and circular states,
  inline activity, steps, paused, complete, error, and content skeleton. A
  skeleton is not the universal loading treatment.

## Maps and location test data

For deterministic map/location evidence, do not use `ICISA Warehouse` as the
warehouse label. Use these test-only addresses when the authorized application
needs a map fixture:

```text
Warehouse
  street: Av. Arnaldo Márquez
  number: 1772
  district: Jesús María
  province: Lima
  region: Lima
  country: Perú

Customer
  street: Av. Sucre
  number: 1992
  district: Pueblo Libre
  province: Lima
  region: Lima
  country: Perú
```

Keep street, number, district, province, region, and country as separate
semantic fields. Use the real maps provider/configuration already approved by
the application; do not hard-code a new provider or claim geolocation support
from a static Lab specimen. Never treat these addresses as production data.

## Responsive and accessibility evidence

Review 1440, 1024, 768, 390, and 320px when the route is responsive. High-risk
surfaces also need 200% text, increased text spacing, 400% reflow, Reduced
Motion, Increased Contrast, visible focus, keyboard/pointer/touch target
evidence, and accessible names/roles/states. Automated evidence does not claim
screen-reader certification, WCAG certification, or replace human review.
