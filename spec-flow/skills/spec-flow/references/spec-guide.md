# Guía: cómo escribir una spec completa y útil

Una spec es el **acuerdo sobre qué se construye y por qué**. La leen negocio (¿es lo que quiero?), desarrollo (¿qué tengo que hacer?), QA (¿cómo lo compruebo?) y los agentes que implementarán. Si alguno de ellos tiene que adivinar, la spec no está terminada.

## Contenido
1. Principios
2. Estructura sección a sección
3. Cómo escribir requisitos
4. Cómo escribir criterios de aceptación
5. Requisitos no funcionales
6. Antipatrones
7. Checklist "spec lista"

## 1. Principios

- **Qué, no cómo.** La spec describe comportamiento observable y resultados. Las tecnologías solo aparecen si son una restricción impuesta ("debe usar el SSO corporativo").
- **Verificable.** Todo requisito debe poder comprobarse con un sí/no. Si no se puede probar, no es un requisito, es un deseo.
- **Atómica.** Un requisito, una cosa. Si lleva "y" o "además", probablemente son dos.
- **Trazable.** Cada elemento tiene ID estable (`REQ-`, `NFR-`, `AC-`). Los IDs no se renumeran: si uno se elimina, se marca como `~~REQ-004~~ (eliminado: motivo)`.
- **Explícita en los límites.** Lo que NO se hace y lo que se ha supuesto sin confirmar valen tanto como lo que se hace.
- **Proporcionada.** Entre 1 y 5 páginas para una funcionalidad; más, y conviene dividir en varias specs.
- **Viva.** Se actualiza cuando cambia el entendimiento, nunca se deja atrás respecto al código.

## 2. Estructura sección a sección

| Sección | Para qué sirve | Está bien cuando… |
|---|---|---|
| Objetivo | Alinear el porqué | Cabe en 2-4 frases y alguien de negocio lo firmaría |
| Métricas de éxito | Saber si mereció la pena | Son resultados medibles tras el lanzamiento ("reducir un 30 % las reservas duplicadas"), no entregables |
| Contexto | Evitar reinventar o romper lo existente | Menciona sistemas afectados, situación actual y motivo del momento |
| Usuarios y escenarios | Diseñar para personas reales | Cada tipo de usuario tiene su objetivo, no solo su nombre |
| Glosario | Un único lenguaje entre negocio y código | Cada término de dominio ambiguo está definido una vez y se usa igual en todo el documento |
| Requisitos funcionales | Qué debe hacer | Cumplen la sección 3 y tienen prioridad |
| Requisitos no funcionales | Cómo de bien debe hacerlo | Todos tienen cifra y método de medida |
| Criterios de aceptación | Cómo se comprueba | Cubren camino feliz, errores y límites de cada requisito |
| Secciones del tipo | Lo que siempre se olvida en frontend/backend/arquitectura | Están todas las de `references/<tipo>.md` |
| Dependencias | Qué necesitamos de otros | Cada dependencia tiene responsable y estado |
| Restricciones | Lo que no es negociable | Separadas de las preferencias |
| Fuera de alcance | Evitar crecimiento descontrolado | No está vacía y responde a lo que alguien podría esperar razonablemente |
| Supuestos | Hacer visibles las apuestas | Cada supuesto dice qué pasaría si es falso |
| Riesgos | Anticipar | Tienen impacto y probabilidad aproximados |
| Preguntas abiertas | No esconder dudas | Las bloqueantes están marcadas `[BLOQUEANTE]`; las resueltas conservan la respuesta |

## 3. Cómo escribir requisitos

Usa el patrón EARS, que obliga a precisar el disparador:

- Siempre: "El sistema debe <respuesta>."
- Evento: "Cuando <disparador>, el sistema debe <respuesta>."
- Estado: "Mientras <estado>, el sistema debe <respuesta>."
- Error: "Si <condición no deseada>, el sistema debe <respuesta>."
- Opcional: "Donde <característica esté activa>, el sistema debe <respuesta>."

Añade prioridad MoSCoW: **[M]** imprescindible, **[S]** debería, **[C]** podría, **[W]** esta vez no (y entonces va a Fuera de alcance).

| ❌ Malo | Problema | ✅ Bueno |
|---|---|---|
| El sistema debe ser fácil de usar | No verificable | NFR: un usuario nuevo completa una reserva sin ayuda en < 2 min (prueba con 5 usuarios) |
| El usuario puede gestionar reservas | "Gestionar" oculta 4 requisitos | REQ-001 crear, REQ-002 consultar, REQ-003 modificar, REQ-004 cancelar |
| Guardar en PostgreSQL con una tabla reservas | Es diseño, no requisito | Las reservas deben persistir tras un reinicio del servicio |
| Validar los datos, etc. | "etc." es trabajo sin definir | Si la franja termina antes de empezar, el sistema debe rechazarla con un error que indique el motivo |
| Notificar al usuario y al administrador y registrar el cambio | Tres requisitos en uno | Tres REQ separados |

## 4. Cómo escribir criterios de aceptación

Formato: `**AC-NNN** (REQ-NNN): Dado <contexto concreto>, cuando <una acción>, entonces <resultado observable>.`

- **Datos concretos**, no genéricos: "una reserva de 10:00 a 11:00" mejor que "una reserva existente".
- **Resultado observable** desde fuera: código de respuesta, mensaje visible, estado consultable. Nunca "el sistema procesa correctamente".
- **Una acción por criterio.**
- **Por cada requisito, piensa en**: camino feliz, entrada inválida, sin permisos, recurso inexistente, límites (vacío, máximo, justo en el borde) y concurrencia si aplica.
- Un AC que repite el requisito con otras palabras no aporta nada: debe añadir un ejemplo que se pueda ejecutar.

Ejemplo débil: *"AC-001: El usuario puede crear una reserva correctamente."*
Ejemplo útil: *"AC-001 (REQ-001): Dado un usuario autenticado y la sala A libre de 10:00 a 11:00, cuando reserva esa franja, entonces recibe confirmación con un identificador y la franja aparece como ocupada al consultar la sala."*

## 5. Requisitos no funcionales

Recorre estas categorías y descarta explícitamente las que no apliquen: rendimiento, escalabilidad, disponibilidad y recuperación (RTO/RPO), seguridad, privacidad y RGPD, accesibilidad, usabilidad, compatibilidad, mantenibilidad, observabilidad, coste, cumplimiento normativo.

Cada NFR necesita: **métrica + umbral + condiciones + cómo se mide**. Por ejemplo: "p95 de la creación de reserva < 300 ms con 50 peticiones/s sostenidas durante 10 min, medido con test de carga en preproducción".

## 6. Antipatrones

- **La spec-solución**: describe clases, tablas y endpoints antes de acordar el comportamiento.
- **Solo camino feliz**: ningún AC de errores, permisos o límites.
- **Adjetivos en vez de cifras**: rápido, seguro, intuitivo, escalable, robusto.
- **Alcance infinito**: "Fuera de alcance" vacío o inexistente.
- **Supuestos escondidos**: decisiones tomadas por Claude que parecen requisitos del usuario.
- **Gold plating**: requisitos que nadie ha pedido pero "estaría bien".
- **Documento zombi**: nadie lo actualiza cuando el código cambia.
- **Datos personales reales** en ejemplos: usa siempre datos ficticios.

## 7. Checklist "spec lista"

- [ ] El objetivo y las métricas de éxito los entendería alguien de negocio.
- [ ] Todos los términos de dominio ambiguos están en el glosario.
- [ ] Cada REQ es atómico, verificable, sigue EARS y tiene prioridad.
- [ ] Cada REQ tiene al menos un AC; los [M] tienen también AC de error o límite.
- [ ] Cada AC tiene datos concretos y un resultado observable.
- [ ] Cada NFR tiene métrica, umbral, condiciones y método de medida.
- [ ] Están todas las secciones obligatorias del tipo.
- [ ] Hay tratamiento explícito de datos personales o se indica que no hay.
- [ ] Fuera de alcance y supuestos no están vacíos.
- [ ] No quedan preguntas `[BLOQUEANTE]` abiertas.
- [ ] No hay decisiones de implementación salvo restricciones impuestas.
