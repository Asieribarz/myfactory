# Referencia: arquitectura

En arquitectura el "producto" son decisiones y estructura, no solo código. La spec describe los **drivers** y el plan describe cómo se valida y materializa la arquitectura.

## Secciones obligatorias en la spec
- **Drivers de negocio**: objetivos, plazos, presupuesto, tamaño y skills del equipo.
- **Atributos de calidad como escenarios medibles** (NFR): "ante un pico de 5.000 usuarios concurrentes, p95 < 500 ms"; "caída de una zona → servicio restaurado en < 5 min". Priorízalos: no se puede maximizar todo.
- **Restricciones**: cloud/on-premise, tecnologías corporativas, normativa (RGPD, residencia de datos), integración con legado.
- **Contexto (C4 nivel 1)**: sistema, usuarios y sistemas externos.
- **Capacidades funcionales** (REQ) a alto nivel.
- **Datos**: tipos de datos, clasificación (personal, sensible), volúmenes, flujos entre sistemas.
- **Operación**: quién lo opera, ventanas de mantenimiento, RTO/RPO.

## Decisiones típicas del plan
Estilo (monolito modular, microservicios, serverless, event-driven), contenedores (C4 nivel 2), comunicación síncrona/asíncrona, almacenamiento por tipo de dato, identidad, despliegue e infraestructura como código, estrategia de migración desde lo existente (strangler fig, big bang...). Cada decisión relevante → ADR.

## Tareas típicas
1. ADRs de las decisiones principales.
2. Spikes / pruebas de concepto para los riesgos más altos (cada una con pregunta concreta y criterio de éxito).
3. Esqueleto andante: un flujo extremo a extremo atravesando todos los contenedores, desplegado.
4. Infraestructura como código y pipeline.
5. Fitness functions: comprobaciones automáticas de los atributos de calidad (tests de carga, reglas de dependencias entre módulos, escaneos de seguridad).

## Verificación típica
ADR aprobado, spike con resultado documentado, esqueleto desplegado, fitness functions en CI.
