# spec-flow

Plugin independiente de myfactory para desarrollar con el método **spec → plan → convergencia → ejecución**: primero se acuerda qué se construye, después cómo, se verifica que ambos encajan y solo entonces se programa.

## Instalación

```text
/plugin marketplace add <tu-usuario>/myfactory
/plugin install spec-flow@myfactory
```

Funciona solo. Si además instalas el plugin `myfactory`, aprovecha sus skills de commits, ADRs y revisión de código.

## Uso

```text
/specflow frontend "panel de administración de usuarios"
/specflow backend "API de reservas de salas" --auto
/specflow arquitectura "migrar facturación a la nube"
/specflow fullstack "portal de clientes"
/specflow continuar 2026-09-24-api-reservas
```

## Fases

| Fase | Qué pasa | Artefacto |
|---|---|---|
| 0. Contexto | Lee el repo, carga la guía del tipo y hace 3-5 preguntas como máximo | `status.md` |
| 1. Spec | Qué y por qué: REQ, NFR medibles, AC Dado/Cuando/Entonces, fuera de alcance | `spec.md` |
| 2. Plan | Cómo: decisiones, riesgos, tareas T-NNN trazadas a la spec | `plan.md` |
| 3. Convergencia | Verificador automático + auditor independiente, hasta 3 rondas | `convergence.md` |
| 4. Ejecución | Una tarea cada vez con test primero y commit por tarea | código + `plan.md` actualizado |
| 5. Cierre | Evidencia de cada AC, revisión, ADRs y resumen | `status.md` = completado |

Todo se guarda en `specs/<fecha>-<slug>/`. En modo supervisado (por defecto) se para tras la spec y tras la convergencia; con `--auto` solo se para ante bloqueos o acciones destructivas.

## Contenido

```
spec-flow/
├── .claude-plugin/plugin.json
├── commands/specflow.md              # comando /specflow
├── agents/
│   ├── spec-plan-auditor.md          # revisa spec y plan en frío
│   └── task-implementer.md           # implementa una tarea con test primero
└── skills/spec-flow/
    ├── SKILL.md                      # el flujo completo
    ├── references/
    │   ├── spec-guide.md             # buenas prácticas y checklist de una spec
    │   ├── plan-guide.md             # buenas prácticas y checklist de un plan
    │   ├── frontend.md               # secciones obligatorias por tipo
    │   ├── backend.md
    │   └── arquitectura.md
    ├── assets/                       # plantillas spec-template.md y plan-template.md
    ├── scripts/check_convergence.py  # verificador de trazabilidad
    └── examples/api-reservas/        # ejemplo completo que converge
```

## Verificador de convergencia

```bash
python3 skills/spec-flow/scripts/check_convergence.py specs/<carpeta>
```

Falla si hay requisitos sin tarea, tareas que no cubren ningún requisito, IDs inexistentes, dependencias circulares, tareas sin verificación o de tamaño L, requisitos sin criterios de aceptación o preguntas `[BLOQUEANTE]` abiertas. Si todo cuadra, imprime el orden de ejecución.
