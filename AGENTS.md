# Repository Working Agreement

## Authority

- `../blueprint/` is the canonical Nexa Product, Domain and accepted architecture
  authority; this repository is support infrastructure, references and
  reproducible tooling.
- `academic/` contains academic sources and projections, `skills/` contains
  skill metadata or snapshots, `library/` contains references, and `tools/`
  contains SCM and validation utilities. None of these areas silently redefine
  Product semantics.
- Inspect the relevant README before modifying a support area and keep
  historical snapshots explicitly historical.

## Repository state

- Inspect the actual branch, worktree, remote metadata and working tree before
  editing.
- Fetch remote metadata before creating new work when permitted; do not merge
  fetched changes into a user's working branch.
- Preserve unrelated local work. Use an isolated worktree when the checkout is
  dirty.

## Tooling and publication boundaries

- Prefer reproducible, secret-free utilities and existing local patterns.
- `construction-environment/` and `structurizr/` contain local construction or
  rendering support; generated caches and host state are not Product runtime
  authority.
- Canonical C4 DSL remains in Blueprint. Do not create a parallel DSL or
  silently rewrite generated evidence to make it appear current.
- Do not publish `.env.local`, private keys, tokens, agent sockets, logs,
  caches, host-specific reports or credential values.
- Do not introduce package managers, services, dependencies or automation
  frameworks merely for a governance change.

## Evidence and security

- Claim only validation, reproducibility, compatibility, acceptance and
  publication results that were actually checked.
- Preserve secret handling, signing boundaries, generated-artifact provenance
  and data integrity.
- Do not weaken security or validation gates to make a tool pass.

## SCM and artifacts

- Preserve real authorship and signatures. Use Conventional Commits where the
  repository policy requires them.
- Do not force-push, rewrite shared history, create fake commits, invent
  contributors, merge automatically, create releases or create tags for this
  governance change.
- Repository-facing artifacts must be neutral, professional and free of
  internal orchestration residue, temporary placeholders and AI attribution.

## Validation and handoff

- Review the task diff and run `git diff --check`. Use the narrowest relevant
  tooling validation for the support area changed.
- Do not claim a build, generated package, signature, publication or CI result
  that was not executed and observed.
- End the task with factual result, changes, validation, commit, risk, open
  decision and unverified-item information.
