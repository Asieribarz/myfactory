---
name: spec-flow
description: Flujo spec-driven completo - especificación (qué y por qué), plan de implementación (cómo), convergencia verificada entre ambos y ejecución tarea a tarea. Úsala cuando el usuario quiera construir algo no trivial (un frontend nuevo, un backend, una API, una arquitectura, una funcionalidad grande), diga "hazme la spec", "spec y plan", "spec-driven", "planifica antes de programar", "specflow" o use el comando /specflow.
---

# Spec-flow: spec → plan → convergencia → ejecución

Separar el **qué** (spec) del **cómo** (plan) y obligar a que converjan antes de escribir código evita el fallo más caro: construir bien lo que no era. Cada fase produce un artefacto en disco para que el proceso sea reanudable, revisable y trazable.

## Parámetros

- **tipo**: `frontend` | `backend` | `arquitectura` | `fullstack`. Si no se indica, dedúcelo de la petición y confírmalo en una línea.
- **descripción**: qué se quiere construir.
- **modo**: `supervisado` (por defecto: para en los puntos de control) o `auto` (solo para si hay bloqueos). Aunque se pida `auto`, para SIEMPRE si hay preguntas bloqueantes sin resolver o antes de acciones destructivas (borrar datos, migraciones irreversibles, push, despliegue).

## Artefactos

Todo vive en `specs/<AAAA-MM-DD>-<slug>/`:

| Fichero | Fase | Contenido |
|---|---|---|
| `spec.md` | 1 | Qué y por qué. Requisitos con IDs. Sin decisiones técnicas salvo restricciones impuestas. |
| `plan.md` | 2 | Cómo. Decisiones técnicas y tareas con IDs que cubren los requisitos. |
| `convergence.md` | 3 | Registro de cada ronda de convergencia: hallazgos y qué se cambió. |
| `status.md` | todas | Fase actual, modo, siguiente paso. Permite reanudar con `/specflow continuar <slug>`. |

## Fase 0 — Contexto

1. Si hay `CLAUDE.md`, léelo. Si el repo es desconocido, haz una exploración ligera (stack, estructura, convenciones, tests) (si está instalado el plugin myfactory, sigue la skill `repo-onboarding`).
2. Lee la referencia del tipo: `references/<tipo>.md` (para `fullstack`, lee `frontend.md` y `backend.md`).
3. Identifica lo que no sabes. Haz al usuario **como máximo 3-5 preguntas**, solo las que cambiarían el diseño. Todo lo demás, resuélvelo como **supuesto explícito** en la spec. En modo `auto` no preguntes: registra supuestos y marca como `[BLOQUEANTE]` solo lo que de verdad impida avanzar.
4. Crea la carpeta y `status.md`.

## Fase 1 — Spec

Lee `references/spec-guide.md` (principios, cómo escribir requisitos EARS y criterios de aceptación, antipatrones y checklist). Rellena `assets/spec-template.md` + las secciones obligatorias de la referencia del tipo. Antes del punto de control, pasa el checklist "spec lista" de la guía. Reglas mínimas:

- Cada requisito funcional es `REQ-NNN`, cada no funcional `NFR-NNN`, cada criterio de aceptación `AC-NNN (REQ-NNN)`, en formato Dado / Cuando / Entonces.
- Todo requisito tiene al menos un AC. Todo NFR es **medible** ("p95 < 300 ms", no "rápido").
- Sección "Fuera de alcance" obligatoria y no vacía.
- Preguntas abiertas: `- [ ] [BLOQUEANTE] ...` o `- [ ] ...`. Resueltas: `- [x] ... → respuesta`.
- Nada de datos personales reales en ejemplos.

**Punto de control (supervisado):** muestra un resumen de la spec (objetivo, nº de REQ/NFR/AC, supuestos, preguntas) y espera aprobación o cambios.

## Fase 2 — Plan

Lee `references/plan-guide.md` (rebanadas verticales, anatomía de una buena tarea, estrategia de pruebas, antipatrones y checklist). Rellena `assets/plan-template.md` y pasa el checklist "plan listo" de la guía. Reglas mínimas:

- Decisiones técnicas relevantes con alternativa descartada y motivo. Las de peso se convertirán en ADRs al ejecutar.
- Tareas `T-NNN`, cada una con: `Cubre:` (REQ/NFR/AC), `Depende de:`, `Ficheros:`, `Verificación:` (qué test o comprobación demuestra que está hecha) y tamaño S/M/L. Ninguna tarea L: divídela.
- Primera tarea: **esqueleto andante** (walking skeleton) extremo a extremo, para validar la integración cuanto antes.
- Orden por riesgo: lo más incierto primero.

## Fase 3 — Convergencia

Bucle de hasta **3 rondas**:

1. **Verificación mecánica**: ejecuta
   `python3 <ruta-skill>/scripts/check_convergence.py specs/<carpeta>`
   Comprueba que todo REQ/NFR/AC está cubierto por alguna tarea, que toda tarea cubre algo (sin trabajo que nadie pidió), que no hay IDs inventados, dependencias rotas o ciclos, tareas sin verificación, ni preguntas bloqueantes abiertas. Imprime además el orden de ejecución.
2. **Auditoría independiente**: lanza el agente `spec-plan-auditor` pasándole solo la ruta de la carpeta (no tu razonamiento: su valor es que lee en frío). Busca contradicciones, ambigüedades, requisitos no verificables, tareas que no cumplen realmente su AC, riesgos no tratados. Si no hay agentes disponibles, haz tú la auditoría con su checklist, releyendo ambos documentos como si no los hubieras escrito.
3. **Corrige en el documento correcto**: si el plan revela que la spec es ambigua o incompleta → cambia la spec. Si el plan no cumple la spec → cambia el plan. Nunca "arregles" la spec para que encaje con un plan cómodo sin decírselo al usuario.
4. Añade la ronda a `convergence.md` (hallazgos → cambios).

Hay convergencia cuando el verificador sale con código 0 **y** el auditor no tiene hallazgos 🔴. Si tras 3 rondas no converge, para y presenta al usuario los puntos en disputa.

**Punto de control (supervisado y también en auto si hubo cambios de alcance):** muestra el resultado de convergencia y el orden de ejecución, y espera el "adelante".

## Fase 4 — Ejecución

Sigue el orden que da el verificador. Para cada tarea:

1. Delega en el agente `task-implementer` pasándole: la tarea completa, los REQ/NFR/AC que cubre (texto copiado de la spec), las decisiones del plan que le afecten y las convenciones del repo. Si no hay agentes, hazlo tú con el mismo procedimiento.
2. El implementador trabaja con test primero a partir de los AC, implementa, ejecuta los tests y devuelve un resumen.
3. Verifica tú el resultado (tests en verde, el AC se cumple de verdad), marca la tarea `- [x]` en `plan.md`, actualiza `status.md` y haz commit en formato Conventional Commits mencionando `T-NNN` (con la skill `commit-message` si está disponible).
4. **Regla de deriva**: si implementar exige apartarse de la spec o del plan, PARA. Actualiza el documento afectado, vuelve a pasar el verificador y, en modo supervisado, pide confirmación. El código nunca diverge en silencio de la spec.

Tareas sin dependencias entre sí pueden lanzarse en paralelo con varios `task-implementer` si no tocan los mismos ficheros.

## Fase 5 — Cierre

1. Recorre todos los AC y confirma cada uno con evidencia (test o comprobación).
2. Revisa el conjunto de cambios con el agente `code-reviewer` si está disponible (plugin myfactory); si no, haz tú una revisión priorizando bugs, seguridad, datos, rendimiento y tests.
3. Crea los ADRs de las decisiones de peso en `docs/adr/NNNN-titulo.md` (contexto, decisión, alternativas, consecuencias), o con la skill `adr` si está disponible.
4. Resume: qué se construyó, AC cumplidos, desviaciones respecto al plan original, deuda pendiente. Actualiza `status.md` a `completado`.

## Reanudar

`/specflow continuar <slug>` → lee `status.md` y continúa en la fase indicada.
