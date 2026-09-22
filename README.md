# Nexa Complementary

Supporting research, references, and reproducible utilities for the Nexa product ecosystem. Complementary does not define Product, Domain, Architecture, runtime behavior, or release readiness; those boundaries are maintained by the authoritative records and implementation repositories.

## Authority boundary

The [Nexa Blueprint](https://github.com/nexa-suite/blueprint) repository is the authority for accepted Product, Domain, C4, technical data, and architecture decisions. This repository may preserve supporting material and reproducible tools, but it must not introduce a competing business or architecture model.

- `academic/` contains academic sources, rubrics, snapshots, and projections. Academic evaluation does not redefine Nexa.
- `catalog-reference/` contains visual and catalog reference material.
- `library/` contains technical and methodological references.
- `skills/` contains operational metadata and snapshots.
- `tools/` contains SCM, validation, and shared utilities.

## Local construction tools

`construction-environment/` and `structurizr/` are local construction and rendering tools. They remain outside the tracked public baseline because they can contain generated artifacts, caches, or machine-specific state. Structurizr consumes the canonical Blueprint workspace; it is not an alternative source of system design.

Use the local README files and scripts when preparing a machine. Do not copy secrets, private paths, credentials, sockets, logs, or host-specific state into the repository.

## Nexa Product Ecosystem

<table>
<tr>
<td><strong><a href="https://github.com/nexa-suite/mobile-report">Mobile Report</a></strong><br>Academic and product research evidence.</td>
<td><strong><a href="https://github.com/nexa-suite/mobile">Mobile</a></strong><br>Accepted mobile projections and implementation workspace.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/nexa-suite/api">API</a></strong><br>Shared backend and domain integration surface.</td>
<td><strong><a href="https://github.com/nexa-suite/website">Website</a></strong><br>Public acquisition and product context.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/nexa-suite/portal">Buyer Portal</a></strong><br>Buyer-facing web experience.</td>
<td><strong><a href="https://github.com/nexa-suite/platform">Platform</a></strong><br>Operations and platform web experience.</td>
</tr>
</table>

## Safe publication

Documentation, manifests, templates, and scripts may be published only when they contain no credentials or machine-local state. Do not publish `.env.local` files, private keys, tokens, agent sockets, logs, caches, host-specific reports, or credential values. Local runtime configuration remains outside version control.

## Structure

```text
complementary/
├── academic/                  sources, rubrics, and labeled projections
├── catalog-reference/         visual and catalog references
├── library/                   technical and methodological library
├── skills/                    operational snapshots and metadata
├── tools/                     validation, SCM, and shared utilities
├── construction-environment/  local-only construction state
└── structurizr/               local-only rendering workspace
```

## Validation and contribution

Start with the local README for the area being changed. Keep supporting material traceable to its source, preserve the distinction between evidence and accepted decisions, and avoid duplicating canonical Product or Domain definitions.

```bash
git diff --check
```

Changes to tools or reference material should include the narrowest applicable validation described by that area. No application runtime, deployment configuration, or Product behavior belongs in this repository.

## Further reading

- [Blueprint authority](https://github.com/nexa-suite/blueprint)
- [Academic material](academic/README.md)
- [Library](library/README.md)
- [Skills](skills/README.md)
- [Tools](tools/)

## Nexa Engineering & Documentation

<table>
<tr>
<td><strong><a href="https://github.com/nexa-suite/blueprint">Blueprint</a></strong><br>Canonical architecture and decision records.</td>
<td><strong><a href="https://github.com/nexa-suite/web-report">Web Report</a></strong><br>Structured report and documentation workspace.</td>
</tr>
<tr>
<td><strong><a href="https://github.com/nexa-suite/complementary">Complementary</a></strong><br>Supporting research and reproducible utilities.</td>
<td><strong><a href="https://github.com/nexa-suite/design-lab">Design Lab</a></strong><br>Executable design-system evidence.</td>
</tr>
</table>

## Legal

Nexa Complementary is maintained for the Nexa project. Consult the repository license and local policy files for permitted use and contribution requirements.
