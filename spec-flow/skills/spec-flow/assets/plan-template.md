# Plan: <título>

- Spec: ./spec.md (versión X)
- Estado: borrador | convergido | en ejecución | completado

## 1. Enfoque
<Un párrafo + diagrama de texto.>

## 2. Decisiones técnicas
| ID | Decisión | Alternativa descartada | Motivo | ¿ADR? |
|---|---|---|---|---|
| D-1 | | | | sí/no |

## 3. Impacto en lo existente
- <Módulo o fichero> — <qué cambia y qué podría romperse>

## 4. Datos y migraciones
<Esquema, migraciones, cómo se revierten; expand/contract si hay datos en producción.>

## 5. Contratos e interfaces
<APIs, eventos, props o tipos compartidos definidos antes de implementar.>

## 6. Riesgos
| Riesgo | Impacto | Mitigación (tarea) |
|---|---|---|

## 7. Hitos
- **H1**: <estado demostrable> — T-001…T-00N

## 8. Tareas
<Orden: esqueleto → riesgos → camino feliz [M] → errores y límites → NFR → pulido.>

### T-001: Esqueleto andante
- [ ] Hecha
- Cubre: REQ-001
- Depende de: —
- Ficheros: <rutas>
- Contexto: <lo mínimo que alguien sin contexto necesita saber>
- Verificación: <test o comprobación concreta>
- Tamaño: S

### T-002: <título>
- [ ] Hecha
- Cubre: REQ-002, AC-002, NFR-001
- Depende de: T-001
- Ficheros: <rutas>
- Contexto: <decisiones D-N que aplican>
- Verificación: <...>
- Tamaño: M

## 9. Estrategia de pruebas
| AC | Nivel (unitario/integración/contrato/e2e/NFR) | Tarea |
|---|---|---|

## 10. Observabilidad
<Logs, métricas y alertas ligados a los NFR. Sin datos personales en logs.>

## 11. Seguridad y privacidad
<Amenazas principales y tratamiento de datos personales, con sus tareas.>

## 12. Despliegue y rollback
<Pasos, feature flags, cómo volver atrás.>

## 13. Definición de hecho (todas las tareas)
- [ ] Tests nuevos y existentes en verde
- [ ] AC demostrados con evidencia
- [ ] Sin secretos ni datos personales
- [ ] Documentación y CLAUDE.md actualizados si procede
