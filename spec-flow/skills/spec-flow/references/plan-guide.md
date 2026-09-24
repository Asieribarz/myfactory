# Guía: cómo escribir un plan de implementación completo y útil

El plan responde a **cómo, en qué orden y cómo sabremos que funciona**. Su lector principal es quien implementa, a menudo un agente que solo verá una tarea cada vez: cada tarea tiene que entenderse por sí sola.

## Contenido
1. Principios
2. Estructura sección a sección
3. Cómo cortar tareas
4. Anatomía de una buena tarea
5. Estrategia de pruebas
6. Antipatrones
7. Checklist "plan listo"

## 1. Principios

- **Trazable a la spec.** Cada tarea cubre IDs de la spec; ninguna aporta alcance nuevo. Si hace falta algo que la spec no pide, se cambia primero la spec.
- **Rebanadas verticales, no capas.** Mejor "crear reserva de punta a punta" que "hacer toda la base de datos" y luego "hacer toda la API".
- **Riesgo primero.** Lo más incierto (integraciones, rendimiento, tecnología nueva) se ataca al principio, cuando cambiar de rumbo aún es barato.
- **Esqueleto andante.** La primera tarea deja un flujo mínimo funcionando y desplegable de extremo a extremo.
- **El sistema siempre funciona.** Cada tarea termina con los tests en verde y se puede commitear sola.
- **Decisiones justificadas.** Cada decisión relevante dice qué alternativa se descartó y por qué.
- **Planificar el fallo.** Migraciones reversibles, feature flags, rollback. Cómo se deshace es parte del plan.

## 2. Estructura sección a sección

| Sección | Para qué sirve | Está bien cuando… |
|---|---|---|
| Enfoque | Visión de conjunto | Un párrafo + diagrama de texto; alguien nuevo entiende la solución en 2 minutos |
| Decisiones técnicas | Hacer explícito el porqué | Cada una con alternativa descartada, motivo y si merece ADR |
| Impacto en lo existente | Evitar sorpresas | Lista módulos y ficheros afectados, y qué podría romperse |
| Datos y migraciones | Proteger los datos | Esquema, migraciones y cómo se revierten; patrón expand/contract si hay datos en producción |
| Contratos e interfaces | Permitir trabajo en paralelo | APIs, eventos o props definidos antes de implementarlos |
| Riesgos | Anticipar | Cada riesgo apunta a la tarea que lo mitiga |
| Hitos | Medir el avance | Cada hito es un estado demostrable, no un porcentaje |
| Tareas | El trabajo | Cumplen la sección 4 |
| Estrategia de pruebas | Demostrar los AC | Cada AC tiene nivel de test asignado |
| Observabilidad | Saber qué pasa en producción | Logs, métricas y alertas ligados a los NFR |
| Seguridad y privacidad | No dejarlo para el final | Amenazas principales y tratamiento de datos personales con tareas propias |
| Despliegue y rollback | Salir a producción sin miedo | Pasos, feature flags y cómo volver atrás |
| Definición de hecho | Criterio común de cierre | Aplica a todas las tareas (tests, revisión, docs, sin secretos) |

## 3. Cómo cortar tareas

- **Tamaño**: S = unas horas; M = uno o dos días. Nada de L. Para agentes, una tarea debe caber en una sesión y tocar pocos ficheros.
- **Una tarea, un resultado verificable.** Si la verificación dice "y además", divídela.
- **Tests dentro de cada tarea**, nunca una tarea final llamada "hacer los tests".
- **Dependencias explícitas y mínimas**: cuantas menos, más paralelismo.
- **Spikes** para lo desconocido: tarea limitada en tiempo, con una pregunta concreta y un criterio de éxito; su resultado alimenta el plan.
- **Orden recomendado**: esqueleto → riesgos altos → camino feliz de los [M] → errores y límites → NFR → pulido.

## 4. Anatomía de una buena tarea

```markdown
### T-002: Crear reserva con control de solapes
- [ ] Hecha
- Cubre: REQ-001, REQ-002, AC-001, AC-002
- Depende de: T-001
- Ficheros: src/reservas.py, migrations/001_reservas.sql, tests/test_reservas.py
- Contexto: usa el repositorio de T-001; el control de solapes va en BD (restricción de exclusión) además de en código, por la concurrencia (decisión D-2).
- Verificación: tests de integración de AC-001 y AC-002 contra BD real en contenedor, incluido un test con 2 peticiones simultáneas a la misma franja.
- Tamaño: M
```

| ❌ Tarea mala | Problema |
|---|---|
| "Backend de reservas" | Enorme, sin verificación, sin trazabilidad |
| "Mejorar el rendimiento" | Sin umbral ni NFR asociado |
| "Crear tablas" | Capa horizontal, no demuestra ningún AC |
| "Tests" al final | Los errores se descubren cuando ya es caro corregirlos |
| "Añadir exportación a Excel" | No está en la spec: gold plating |

## 5. Estrategia de pruebas

Asigna cada AC al nivel más bajo que lo demuestre de verdad:

- **Unitario**: reglas de dominio y cálculos.
- **Integración**: persistencia, colas, APIs con dependencias reales en contenedor.
- **Contrato**: acuerdos entre frontend y backend o entre servicios.
- **Extremo a extremo**: solo los flujos críticos; son lentos y frágiles.
- **No funcionales**: carga, accesibilidad, seguridad, con umbrales que fallan en CI.

Los datos de prueba siempre son ficticios.

## 6. Antipatrones

- **Plan-lista de deseos**: tareas que nadie ha pedido.
- **Big bang**: todo se integra al final.
- **Capas horizontales**: semanas sin nada que se pueda probar.
- **Tareas vagas**: "revisar", "mejorar", "ajustar".
- **Dependencias ocultas**: una tarea necesita algo que no declara.
- **Sin rollback**: migraciones irreversibles o despliegues sin vuelta atrás.
- **Re-especificar**: el plan cambia el comportamiento acordado sin tocar la spec.
- **Decisiones sin alternativa**: "usaremos X" sin decir por qué no Y.

## 7. Checklist "plan listo"

- [ ] Cada tarea cubre IDs de la spec y ninguna añade alcance.
- [ ] Todo REQ, NFR y AC está cubierto (lo confirma `check_convergence.py`).
- [ ] T-001 es un esqueleto andante extremo a extremo.
- [ ] Los riesgos altos se atacan en las primeras tareas.
- [ ] Ninguna tarea es L y todas tienen verificación concreta.
- [ ] Cada tarea deja el sistema funcionando y se puede commitear sola.
- [ ] Las decisiones relevantes tienen alternativa y motivo.
- [ ] Hay estrategia de pruebas por AC y de datos ficticios.
- [ ] Migraciones, despliegue y rollback están descritos.
- [ ] Seguridad, privacidad y observabilidad tienen tareas propias.
- [ ] Una persona o agente sin contexto podría ejecutar cualquier tarea leyendo solo esa tarea y la spec.
