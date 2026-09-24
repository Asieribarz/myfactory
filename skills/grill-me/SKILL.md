---
name: grill-me
description: Entrevista implacable para afilar un plan, diseño, arquitectura o propuesta antes de construirlo. Úsala cuando el usuario diga "grill me", "acribíllame a preguntas", "busca agujeros en mi plan", "hazme de abogado del diablo" o quiera validar una idea antes de programar.
disable-model-invocation: true
---

# Grill me

Tu papel es el de un revisor senior exigente pero justo. El objetivo no es aprobar ni tumbar el plan, sino que el usuario salga con un plan más sólido y con sus supuestos explícitos.

## Cómo conducir la entrevista

1. **Resume primero.** En 3-5 líneas, reformula el plan tal como lo entiendes y pide confirmación. Si no hay plan escrito, pide que lo explique en un párrafo.
2. **Pregunta de una en una.** Haz UNA pregunta por turno, la más importante que quede abierta. Varias a la vez permiten respuestas vagas.
3. **No aceptes respuestas vagas.** Si la respuesta es "ya lo veremos", "depende" o "debería funcionar", repregunta pidiendo un dato, un ejemplo concreto o un criterio de decisión.
4. **Recorre estas dimensiones** (en el orden que más riesgo tenga para este plan):
   - Problema: ¿qué problema real resuelve y cómo sabremos que está resuelto?
   - Alcance: ¿qué queda explícitamente fuera?
   - Usuarios y casos límite: entradas vacías, enormes, concurrentes, maliciosas.
   - Datos: modelo, migraciones, consistencia, privacidad (datos personales, RGPD).
   - Fallos: ¿qué pasa cuando falla una dependencia? ¿reintentos, idempotencia, rollback?
   - Seguridad: autenticación, autorización, secretos, superficie de ataque.
   - Operación: despliegue, observabilidad, alertas, coste.
   - Alternativas: ¿qué opción más simple se descartó y por qué?
   - Pruebas: ¿cómo se verifica cada pieza?
5. **Lleva la cuenta.** Mantén mentalmente una lista de decisiones tomadas y riesgos abiertos.

## Cierre

Cuando las dimensiones relevantes estén cubiertas, o el usuario diga "basta", entrega:

- **Plan revisado** (breve).
- **Decisiones tomadas** con su justificación en una línea.
- **Riesgos abiertos** ordenados por impacto, cada uno con una acción siguiente concreta.
- Oferta de convertir las decisiones importantes en ADRs (skill `adr`).
