---
description: Prepara un cambio para entregar - escaneo de secretos, tests, commit y descripción de PR
argument-hint: [notas opcionales para el commit]
---

Prepara el trabajo actual para entregarlo, en este orden y parando si algo falla:

1. **Secretos/PII**: aplica la skill `secrets-guard` sobre los cambios en staging. Si hay hallazgos, detente y propón cómo corregirlos.
2. **Tests**: ejecuta los tests del proyecto (usa el agente `test-runner` si está disponible). Si fallan, detente.
3. **Commit**: aplica la skill `commit-message`. Notas del usuario: $ARGUMENTS
4. **PR**: aplica la skill `pr-description` y muestra la descripción lista para pegar.

No hagas `git push` sin confirmación explícita.
