---
name: secrets-guard
description: Detecta credenciales, claves API, tokens, cadenas de conexión y datos personales (emails, DNI/NIE, IBAN, teléfonos) en código, diffs y ficheros antes de commitear o compartir. Úsala siempre antes de un commit o push, cuando el usuario pida "revisa si hay secretos", "¿puedo subir esto?", "auditoría RGPD del repo", o cuando vayas a pegar código o logs en otro sitio.
---

# Guardia de secretos y datos personales

## Escaneo

Ejecuta el escáner incluido (Python 3, sin dependencias):

```bash
python3 <ruta-skill>/scripts/scan_secrets.py --staged      # solo lo que va al commit
python3 <ruta-skill>/scripts/scan_secrets.py                # todos los ficheros versionados
python3 <ruta-skill>/scripts/scan_secrets.py ruta/a/fichero # ficheros concretos
```

El escáner enmascara los valores encontrados: nunca los imprime completos. Código de salida 1 si hay hallazgos.

## Interpretación

- Valores con marcadores evidentes de prueba (`test`, `dummy`, `example`, `changeme`, `xxx`, `1234`, `TU_CLAVE_AQUI`) se ignoran automáticamente.
- Para falsos positivos puntuales, añade `# secrets-guard: ignore` al final de la línea o la ruta a `.secretsignore` (un glob por línea).

## Si hay hallazgos reales

1. **No los repitas** en tu respuesta: refiérete a ellos por `fichero:línea` y tipo.
2. Sustitúyelos por variables de entorno o un gestor de secretos, y deja un placeholder en `.env.example`.
3. Asegúrate de que `.env` está en `.gitignore`.
4. Si el secreto ya se commiteó o se subió: **rotarlo es obligatorio** (borrarlo del historial no basta). Después, si hace falta, limpiar historial con `git filter-repo`.
5. Para datos personales: anonimiza con datos ficticios (`[NOMBRE_ANONIMIZADO]`, `usuario@example.com`) en fixtures, tests, logs y documentación.
