---
name: adr
description: Crea Architecture Decision Records (ADR) para documentar decisiones técnicas en docs/adr/. Úsala cuando el usuario diga "documenta esta decisión", "crea un ADR", "¿por qué elegimos X?" o después de una sesión de grill-me con decisiones relevantes.
---

# ADRs

1. Busca `docs/adr/` (o `doc/adr/`, `adr/`). Si no existe, créalo.
2. Numera con el siguiente número libre: `0001-titulo-en-kebab-case.md`.
3. Usa la plantilla `templates/docs/adr-template.md` de myfactory (copiada abajo si no está disponible).
4. Si la decisión sustituye a otra, actualiza el estado del ADR antiguo a "Sustituido por ADR-XXXX".

```markdown
# ADR-XXXX: <Título>

- Estado: Propuesto | Aceptado | Rechazado | Sustituido por ADR-YYYY
- Fecha: AAAA-MM-DD

## Contexto
<Fuerzas en juego, restricciones, problema>

## Decisión
<Qué se decide, en voz activa: "Usaremos...">

## Alternativas consideradas
- <Opción>: <por qué no>

## Consecuencias
- Positivas: ...
- Negativas / deuda asumida: ...
```

Sé concreto y breve: un ADR debe leerse en 2 minutos.
