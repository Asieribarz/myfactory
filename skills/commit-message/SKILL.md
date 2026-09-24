---
name: commit-message
description: Genera mensajes de commit claros siguiendo Conventional Commits a partir de los cambios en staging. Úsala siempre que el usuario pida hacer un commit, "escribe el mensaje de commit", "commitea esto" o cuando termines un cambio y vayas a confirmarlo.
---

# Mensajes de commit

## Proceso

1. Ejecuta `git diff --staged` (si está vacío, `git status` y pregunta qué añadir; no hagas `git add -A` sin confirmar).
2. Si el diff mezcla cambios no relacionados, propón dividirlo en varios commits.
3. Revisa `git log --oneline -15` para respetar el estilo que ya use el repo (idioma, scopes). Si el repo ya tiene convención propia, esa manda.
4. Escribe el mensaje.

## Formato

```
<tipo>(<scope opcional>): <resumen en imperativo, ≤ 72 caracteres, sin punto final>

<cuerpo opcional: el porqué del cambio, no el cómo; líneas de ≤ 72>

<footer opcional: BREAKING CHANGE: ..., Refs #123>
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

## Ejemplos

- `feat(auth): añade renovación automática de sesión`
- `fix(api): evita doble cobro al reintentar pagos`
- `refactor: extrae validación de formularios a un módulo común`

## Reglas

- El resumen describe el efecto, no el fichero ("corrige el cálculo de IVA", no "cambia utils.py").
- Nunca incluyas secretos, tokens ni datos personales en el mensaje.
- Antes de commitear, si existe `scripts/scan_secrets.py` o la skill `secrets-guard`, pásalo sobre el diff.
