# Design Lab validation

Run commands from `/Users/diegosandoval284/Developer/nexa-suite/design-lab` after
checking the current branch and source SHA. Choose the smallest set that
matches the change, but do not claim a full release from a partial gate.

## Deterministic gates

The full Design Lab gate set is:

```bash
npm ci
npm test -- --watch=false
npm run test:library -- --watch=false
npm run build
npm run build:library
npm run build:all
npm run validate:architecture
npm run validate:tokens
npm run validate:colors
npm run validate:icons
npm run validate:documentation
npm run validate:public-api
npm run validate:visual
npm run validate:contrast
npm run validate:package
npm run validate:browser
git diff --check
```

`npm run audit:visual` is a review aid after the browser gate. It writes
ignored evidence under `tmp/`; it does not turn human visual review into an
automated pass.

## What each gate protects

- Architecture: reusable token boundaries, geometry, forbidden CSS,
  dependency direction, package-source singularity, retired imports, and
  tracked FLOW assets.
- Tokens/colors/icons: canonical token generation, documented color math, and
  the local approved PrimeIcons pipeline.
- Documentation/visual: focused route features, registry coverage, canonical
  state matrices, required viewports, and no catch-all renderer regression.
- Public API/package: explicit reusable exports only; no documentation, Lab,
  source, or generated leakage into `nexa-ui`.
- Contrast: WCAG 2.2 evidence contracts (4.5:1 normal text, 3:1 large text
  and essential non-text UI) using token values.
- Browser: routes, viewport matrix, console/page errors, overflow, heading and
  active-navigation behavior, state/recovery interactions, locale, Action
  Menu, Tooltip, motion, text spacing, and evaluation modes.

## Application handoff evidence

When adopting a candidate in Platform or Portal, record:

- Design Lab source SHA/tag.
- Blueprint baseline/decision.
- Public API and token version.
- Responsive and contrast evidence.
- Application test/build result.
- Authenticated browser evidence for the real route and permission path.
- Human visual and assistive-technology review status.

A Design Lab browser pass does not prove API integration, tenant isolation,
authorization, backend state transitions, or production readiness.

## Failure handling

Stop and report the exact command, repository, branch, SHA, and output when a
required gate fails. Do not weaken a validator, hide console errors, delete
evidence, or mark a candidate complete because another repository passed.
