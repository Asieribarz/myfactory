---
name: repo-onboarding
description: Explora un repositorio desconocido y genera un mapa del proyecto y un CLAUDE.md con comandos, arquitectura y convenciones. Úsala cuando el usuario empiece a trabajar en un repo nuevo, diga "explícame este repo", "¿cómo funciona este proyecto?", "prepara el CLAUDE.md" o "onboarding".
---

# Onboarding de repositorio

## Exploración (solo lectura)

1. Estructura: `git ls-files | head -300` y árbol de primer y segundo nivel.
2. Manifiestos: `package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.csproj`, `Dockerfile`, `docker-compose*`, `Makefile`.
3. Documentación existente: `README*`, `CONTRIBUTING*`, `docs/`, `CLAUDE.md`, `AGENTS.md`.
4. CI: `.github/workflows/`, `.gitlab-ci.yml`, etc. → revelan los comandos reales de build/test/lint.
5. Puntos de entrada y 2-3 flujos principales siguiéndolos por el código.
6. Historial: `git log --oneline -30` y `git shortlog -sn --no-merges | head` (no reproduzcas nombres personales en el resultado; resume como "N contribuidores").

## Entregables

1. **Resumen para el usuario**: qué hace el proyecto, stack, arquitectura en un diagrama de texto, cómo arrancarlo, cómo testear, zonas delicadas.
2. **CLAUDE.md** (si no existe, o propón un diff si existe) usando `templates/CLAUDE.md` del repo myfactory como base, con:
   - Comandos exactos (instalar, dev, test, lint, build).
   - Mapa de directorios con una línea por carpeta importante.
   - Convenciones de código y de commits observadas.
   - Cosas que NO hay que tocar o que tienen trampa.

No inventes comandos: si no puedes confirmarlo en el repo, márcalo como `TODO: verificar`.
