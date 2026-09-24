# myfactory 🏭

Mi fábrica personal de **skills, agentes, comandos, hooks y plantillas** para Claude Code (y Claude.ai), reutilizable en todos los repos en los que trabajo.

Este repo es un *marketplace* con dos plugins independientes:

| Plugin | Carpeta | Qué es |
|---|---|---|
| `myfactory` | raíz | Utilidades de trabajo diario (este README) |
| `spec-flow` | [`spec-flow/`](spec-flow/) | Flujo spec → plan → convergencia → ejecución ([ver su README](spec-flow/README.md)) |

## Qué incluye

| Tipo | Nombre | Para qué |
|---|---|---|
| Skill | `grill-me` | Entrevista implacable para afilar un plan antes de construirlo (solo invocación manual: `/grill-me`) |
| Skill | `commit-message` | Mensajes de commit con Conventional Commits |
| Skill | `pr-description` | Descripción de PR a partir de la rama |
| Skill | `code-review` | Revisión priorizada: bugs > seguridad > datos > rendimiento > tests > estilo |
| Skill | `repo-onboarding` | Mapa de un repo nuevo + generación de `CLAUDE.md` |
| Skill | `systematic-debugging` | Depuración por hipótesis con test de regresión |
| Skill | `write-tests` | Tests en el framework y estilo del repo |
| Skill | `adr` | Architecture Decision Records en `docs/adr/` |
| Skill | `changelog` | `CHANGELOG.md` (Keep a Changelog) + versión SemVer |
| Skill | `secrets-guard` | Detecta secretos y datos personales (RGPD) con un escáner Python sin dependencias |
| Agente | `code-reviewer` | Segunda opinión independiente sobre un diff |
| Agente | `test-runner` | Ejecuta tests y analiza fallos |
| Comando | `/ship` | secrets-guard → tests → commit → descripción de PR |
| Comando | `/onboard` | Onboarding del repo actual |
| Hook | `pre_commit_guard` | Bloquea `git commit` desde Claude si hay secretos en staging |

## Instalación

### Opción A — Plugin de Claude Code (recomendada)

```text
/plugin marketplace add <tu-usuario>/myfactory
/plugin install myfactory@myfactory   # utilidades
/plugin install spec-flow@myfactory   # flujo spec-driven
```

Puedes instalar uno, otro o los dos.

Actualizar tras hacer cambios en el repo: `/plugin marketplace update myfactory`.

### Opción B — Copiar skills a mano

```bash
git clone https://github.com/<tu-usuario>/myfactory.git ~/myfactory
~/myfactory/scripts/install.sh --link            # global en ~/.claude (symlinks, se actualiza con git pull)
~/myfactory/scripts/install.sh /ruta/a/mi-repo   # solo para un repo concreto
```

### Opción C — Claude.ai

Comprime una carpeta de `skills/` (p. ej. `skills/code-review`) en un `.zip` y súbela en *Settings → Capabilities → Skills*.

## Preparar un repo nuevo

```bash
~/myfactory/scripts/bootstrap-repo.sh /ruta/a/mi-repo
```

Añade (sin sobrescribir nada existente): `CLAUDE.md`, `.editorconfig`, `.gitignore`, `.env.example`, `.pre-commit-config.yaml`, `.secretsignore`, plantillas de PR e issues, plantilla de ADR y un hook `pre-commit` de git con secrets-guard.

## Escáner de secretos

```bash
python3 skills/secrets-guard/scripts/scan_secrets.py --staged   # antes de commitear
python3 skills/secrets-guard/scripts/scan_secrets.py            # todo el repo
```

Detecta claves privadas, tokens (AWS, GitHub, GitLab, Slack, Anthropic/OpenAI, Google, Stripe), JWT, Bearer, cadenas de conexión, Tenant/Client IDs y asignaciones tipo `password = "..."`; y como PII: emails, DNI/NIE (con letra de control), IBAN (con dígito de control) y teléfonos españoles. Nunca imprime los valores completos. Ignora marcadores de prueba (`test`, `dummy`, `example`, `TU_CLAVE_AQUI`...), líneas con `# secrets-guard: ignore` y rutas en `.secretsignore`.

## Crear una skill nueva

```bash
./scripts/new-skill.sh mi-skill     # esqueleto en skills/mi-skill/SKILL.md
python3 scripts/validate_skills.py  # valida frontmatter (también corre en CI)
```

Consejo: la `description` es lo que decide cuándo se activa la skill. Incluye qué hace **y** frases concretas que dirías para pedirlo.

## Estructura

```
myfactory/
├── .claude-plugin/        # marketplace.json (lista los 2 plugins) + plugin.json
├── spec-flow/             # plugin spec-flow, autocontenido
├── skills/<nombre>/SKILL.md
├── agents/                # subagentes
├── commands/              # slash commands
├── hooks/                 # hooks de Claude Code
├── scripts/               # install, bootstrap, new-skill, validate
├── templates/             # ficheros base para repos
└── .github/workflows/     # CI de validación
```
