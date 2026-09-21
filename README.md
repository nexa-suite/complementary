# Nexa Complementary

Repositorio público de soporte, referencias y herramientas reproducibles para
el ecosistema Nexa Suite. Complementary no es autoridad de Product, Domain ni
Architecture: esa autoridad vive en `nexa-suite/blueprint`.

## Límites de autoridad

- `../blueprint/` contiene el canon vigente de Product, DDD, C4, PostgreSQL y
  decisiones aceptadas.
- `academic/` conserva fuentes académicas, rúbricas y proyecciones etiquetadas;
  la rúbrica controla cumplimiento académico, no redefine Nexa.
- `skills/` contiene metadatos y snapshots operativos; una skill no es
  autoridad de Product.
- `library/` contiene referencias técnicas y metodológicas.
- `tools/` contiene utilidades de SCM y validación.

## Herramientas de construcción

`construction-environment/` y `structurizr/` son herramientas locales de
construcción y renderizado. Permanecen ignoradas por Git porque incluyen
artefactos generados, cachés y estado de una máquina. El runtime Structurizr
lee el workspace C4 canónico de Blueprint; no contiene un DSL alternativo.

Para preparar una máquina, usa los README y scripts locales de esas carpetas,
sin copiar secretos ni rutas privadas al repositorio público.

## Publicación segura

Se pueden publicar documentación, manifests, plantillas y scripts sin
secretos. No se publican `.env.local`, claves privadas, tokens, sockets de
agente, logs, caches, reportes host-específicos ni valores de credenciales.
`tools/runtime/*.env` es estado local ignorado; cada colaborador genera su
propia configuración fuera de Git.

## Estructura

```text
complementary/
├── academic/       fuentes, rúbricas y snapshots/proyecciones etiquetados
├── catalog-reference/  referencias visuales de catálogo
├── library/        biblioteca técnica y metodológica
├── skills/         snapshot histórico y baseline actual de skills
├── tools/          validación, SCM y utilidades compartidas
├── construction-environment/  local-only
└── structurizr/    local-only; consume ../blueprint
```

Consulta siempre Blueprint antes de modificar una semántica de Nexa. Los
repositorios de aplicaciones son evidencia de implementación, no una fuente
para redefinir el canon.
