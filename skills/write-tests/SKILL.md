---
name: write-tests
description: Escribe o mejora tests unitarios y de integración siguiendo el framework y estilo del repo. Úsala cuando el usuario pida "añade tests", "sube la cobertura", "testea esta función", "TDD" o tras implementar una funcionalidad sin tests.
---

# Escribir tests

## Antes de escribir

1. Detecta el framework y convenciones mirando tests existentes (pytest, unittest, Jest, Vitest, JUnit, xUnit, Go test...). Imita su estructura, nombres, fixtures y ubicación.
2. Localiza el comando real para ejecutarlos (CI, `package.json`, `Makefile`).

## Qué probar

- Camino feliz.
- Casos límite: vacío, uno, muchos, límites numéricos, unicode, nulos.
- Errores: entradas inválidas, dependencias que fallan, timeouts.
- Regresiones de bugs conocidos.

## Cómo

- Prueba comportamiento observable, no detalles internos.
- Un concepto por test; nombre que describa el escenario y el resultado esperado.
- Patrón Arrange / Act / Assert.
- Mockea solo fronteras (red, disco, reloj, servicios externos).
- Datos de prueba ficticios y evidentes (`usuario@example.com`, `TEST_KEY`), nunca datos reales.

## Cierre

Ejecuta los tests. Si alguno falla, determina si el fallo está en el test o revela un bug real, y dilo. Informa de cobertura si hay herramienta configurada.
