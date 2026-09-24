---
name: systematic-debugging
description: Depuración metódica basada en hipótesis para bugs, tests que fallan, errores en producción o comportamientos raros. Úsala cuando el usuario diga "no funciona", "da error", "este test falla", "¿por qué pasa esto?" o pegue un stack trace.
---

# Depuración sistemática

No propongas un arreglo hasta entender la causa. Los parches a ciegas esconden el bug.

## Bucle

1. **Reproducir**: consigue un comando o test mínimo que falle de forma determinista. Si no se reproduce, recoge más datos (logs, versión, entorno, entrada exacta).
2. **Acotar**: ¿desde cuándo falla? Usa `git log`, `git bisect` o compara con una versión que funcione. Reduce la entrada al mínimo que falla.
3. **Hipótesis**: enumera 2-4 causas posibles, ordenadas por probabilidad × facilidad de comprobar.
4. **Experimento**: para cada hipótesis, una comprobación que la confirme o descarte (log, breakpoint, assert, test). Cambia una sola cosa cada vez.
5. **Causa raíz**: pregunta "¿por qué?" hasta llegar a algo accionable.
6. **Arreglo + test de regresión**: primero un test que falle por el bug, después el arreglo, después comprobar que pasa y que no rompe otros tests.

## Salida

Al final, resume: síntoma → causa raíz → arreglo → test añadido → si hay otros sitios con el mismo patrón.
