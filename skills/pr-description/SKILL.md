---
name: pr-description
description: Redacta la descripción de una Pull Request / Merge Request a partir de los commits y el diff de la rama. Úsala cuando el usuario pida "abre una PR", "descripción de la PR", "resume los cambios de la rama" o vaya a mergear.
---

# Descripción de PR

## Proceso

1. Detecta la rama base (`main`/`master`/`develop`): `git merge-base HEAD origin/main`.
2. Lee `git log --oneline base..HEAD` y `git diff --stat base..HEAD`, luego el diff completo de los ficheros clave.
3. Si el repo tiene `.github/pull_request_template.md`, rellena esa plantilla. Si no, usa la de abajo.

## Plantilla

```markdown
## Qué cambia
<2-4 frases orientadas al revisor>

## Por qué
<problema o issue que resuelve; enlaza "Closes #N" si aplica>

## Cómo probarlo
1. ...
2. ...

## Riesgos y notas para el revisor
- <migraciones, flags, cambios de contrato, rendimiento>

## Checklist
- [ ] Tests añadidos o actualizados
- [ ] Documentación actualizada
- [ ] Sin secretos ni datos personales en el código
```

## Reglas

- Título en formato Conventional Commits (`feat: ...`).
- Señala explícitamente los breaking changes.
- Si la PR es muy grande (> ~400 líneas de lógica), sugiere cómo dividirla.
