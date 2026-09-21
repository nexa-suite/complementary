# Shared Structurizr runtime tooling

Team-reproducible local workbench. Blueprint owns one canonical C4 DSL; this
directory owns only safe runtime tooling. No semantic DSL is edited here.

Structurizr tooling != Nexa runtime. Structurizr Docker service != C4 Container.
Blueprint owns architecture semantics and remains the only C4 source of truth.

Expected workspace layout:

```text
nexa-suite/
  blueprint/
  complementary/structurizr/
```

From `complementary/structurizr`:

```bash
# Optional: point at another checked-out Blueprint worktree.
export NEXA_BLUEPRINT_DIR="../../blueprint"
docker compose config -q
docker compose up -d
docker compose ps
curl -fsS http://127.0.0.1:9090/
docker compose logs --tail=100 structurizr
docker compose down
```

Compose project name is `nexa-blueprint-architecture`; local mapping is
`127.0.0.1:9090` to container port `8080`. Canonical Blueprint input mounts
read-only into a small seed helper, then copies into an ignored writable runtime
volume required by Structurizr Local. The copy is generated runtime state, not a
second source of truth. Edit DSL only under Blueprint.
