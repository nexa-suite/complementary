# Local runtime signer state

Files in this directory are per-machine runtime configuration for local
contributors. They may contain credentials or signing-agent references and
must never be committed. `.gitignore` excludes `tools/runtime/*.env` and local
logs.

Create or update these files through the approved local setup helpers. Use
templates and environment variables; do not place secret values in tracked
documentation, manifests or scripts. This directory is not an authority for
Nexa Product, Domain or Architecture.
