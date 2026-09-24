# Spec: API de reservas de salas

- Tipo: backend
- Estado: aprobada
- Fecha: 2026-09-24

## 1. Objetivo
Permitir a los empleados reservar salas de reuniones sin solapamientos.

## 4. Requisitos funcionales
- **REQ-001**: Un usuario autenticado puede crear una reserva de una sala para una franja horaria.
- **REQ-002**: El sistema impide reservas solapadas en la misma sala.
- **REQ-003**: Un usuario puede cancelar sus propias reservas.

## 5. Requisitos no funcionales
- **NFR-001**: p95 de creación de reserva < 300 ms con 50 peticiones/s.
- **NFR-002**: Los logs no contienen datos personales (0 coincidencias en un escaneo automático de PII).

## 6. Criterios de aceptación
- **AC-001** (REQ-001): Dado un usuario autenticado y una sala libre, cuando crea una reserva, entonces recibe 201 y la reserva queda guardada.
- **AC-002** (REQ-002): Dada una reserva existente de 10:00 a 11:00, cuando otro usuario pide 10:30 a 11:30 en la misma sala, entonces recibe 409.
- **AC-003** (REQ-003): Dado un usuario con una reserva, cuando la cancela, entonces recibe 204 y la franja queda libre.
- **AC-004** (REQ-003): Dado un usuario, cuando intenta cancelar una reserva ajena, entonces recibe 403.

## 9. Fuera de alcance
- Reservas recurrentes.
- Integración con calendarios externos.

## 11. Preguntas abiertas
- [x] [BLOQUEANTE] ¿Qué proveedor de identidad? → El SSO corporativo vía OIDC.
- [ ] ¿Se notificará por email? (no bloquea la v1)
