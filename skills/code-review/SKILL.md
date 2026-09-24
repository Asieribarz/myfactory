---
name: code-review
description: Revisión de código rigurosa de un diff, rama, PR o fichero, priorizando bugs, seguridad y mantenibilidad. Úsala cuando el usuario pida "revisa este código", "code review", "¿ves algún problema?", "revisa mi PR" o antes de mergear.
---

# Code review

## Alcance

Revisa lo que se indique; si no se indica nada, revisa `git diff` (sin staging) + `git diff --staged`. Lee el contexto alrededor de cada cambio, no solo las líneas modificadas.

## Qué buscar, por orden de prioridad

1. **Corrección**: lógica errónea, off-by-one, nulos, condiciones de carrera, errores tragados, casos límite.
2. **Seguridad**: inyección (SQL, comandos, XSS), autorización ausente, secretos en código, deserialización insegura, datos personales en logs.
3. **Datos**: migraciones irreversibles, pérdida de datos, transacciones.
4. **Rendimiento**: N+1, bucles costosos, falta de índices, cargas completas en memoria.
5. **Tests**: ¿cubren el cambio? ¿prueban comportamiento o implementación?
6. **Mantenibilidad**: nombres, duplicación, complejidad, acoplamiento.
7. **Estilo**: solo si no lo cubre un linter.

## Formato de salida

Agrupa los hallazgos por severidad:

- 🔴 **Bloqueante**: debe corregirse antes de mergear.
- 🟡 **Importante**: debería corregirse.
- 🔵 **Sugerencia**: opcional.

Cada hallazgo: `ruta:línea`, qué pasa, por qué importa y la corrección propuesta (con fragmento de código si ayuda). Termina con un veredicto de una línea. Si todo está bien, dilo sin inventar problemas.
