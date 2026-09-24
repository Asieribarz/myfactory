# Referencia: backend

## Secciones obligatorias en la spec
- **Modelo de dominio**: entidades, relaciones, invariantes ("una reserva no puede solaparse con otra").
- **Contrato de API**: endpoints/operaciones o eventos, entradas, salidas, códigos de error y su significado, versionado. Formato OpenAPI si es REST.
- **Autenticación y autorización**: quién puede hacer qué (matriz rol × operación).
- **Persistencia**: qué se guarda, retención, migraciones, volumen esperado.
- **Consistencia y concurrencia**: idempotencia de operaciones reintentables, transacciones, qué pasa con peticiones simultáneas.
- **Integraciones**: servicios externos, qué pasa cuando fallan (timeouts, reintentos, circuit breaker).
- **Rendimiento y disponibilidad** (NFR): latencia p95/p99, throughput, SLO de disponibilidad.
- **Seguridad** (NFR): validación de entradas, OWASP Top 10, gestión de secretos, rate limiting.
- **Datos personales / RGPD** (NFR): qué datos personales se tratan, base legal, minimización, retención y borrado, cifrado, no aparecer en logs.
- **Observabilidad**: logs estructurados, métricas, trazas, alertas.

## Decisiones típicas del plan
Lenguaje y framework, arquitectura interna (capas/hexagonal), base de datos, ORM y migraciones, colas, caché, estrategia de errores, configuración y secretos.

## Tareas típicas
1. Esqueleto: servicio arrancando con un endpoint de salud, conexión a BD, pipeline de CI, desplegable.
2. Modelo y migraciones.
3. Una tarea por operación o grupo de operaciones, con sus errores.
4. AuthN/AuthZ.
5. Observabilidad y NFR medibles (test de carga) como tareas propias.

## Verificación típica
Unitarios de dominio, integración con BD real en contenedor, tests de contrato de la API, test de carga para NFR de rendimiento.
