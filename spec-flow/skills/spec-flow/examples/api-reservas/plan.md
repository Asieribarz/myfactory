# Plan: API de reservas de salas

## 4. Tareas

### T-001: Esqueleto andante
- [ ] Hecha
- Cubre: REQ-001
- Depende de: —
- Ficheros: src/app.py, tests/test_health.py
- Verificación: GET /health devuelve 200 en CI con BD en contenedor
- Tamaño: S

### T-002: Crear reserva con control de solapes
- [ ] Hecha
- Cubre: REQ-001, REQ-002, AC-001, AC-002
- Depende de: T-001
- Ficheros: src/reservas.py, migrations/001_reservas.sql
- Verificación: tests de integración AC-001 y AC-002, incluido test concurrente
- Tamaño: M

### T-003: Cancelar reserva
- [ ] Hecha
- Cubre: REQ-003, AC-003, AC-004
- Depende de: T-002
- Ficheros: src/reservas.py
- Verificación: tests de integración AC-003 y AC-004
- Tamaño: S

### T-004: Rendimiento y privacidad de logs
- [ ] Hecha
- Cubre: NFR-001, NFR-002
- Depende de: T-002
- Ficheros: tests/load/, src/logging.py
- Verificación: test de carga k6 con umbral p95<300ms y escaneo de PII sobre logs de prueba
- Tamaño: M
