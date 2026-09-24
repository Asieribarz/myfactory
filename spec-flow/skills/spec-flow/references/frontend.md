# Referencia: frontend

## Secciones obligatorias en la spec
- **Pantallas y rutas**: lista de vistas con su propósito y quién accede.
- **Flujos de usuario**: pasos de los 2-4 flujos principales.
- **Estados de cada vista**: cargando, vacío, error, éxito, sin permisos. Cada estado relevante necesita un AC.
- **Contrato de datos consumido**: endpoints/eventos que usa, forma de los datos, qué pasa si fallan o tardan.
- **Accesibilidad** (NFR): nivel WCAG 2.2 AA por defecto; navegación por teclado, foco, contraste, lectores de pantalla.
- **Responsive** (NFR): breakpoints y dispositivos objetivo.
- **Rendimiento** (NFR): presupuestos medibles, p. ej. LCP < 2,5 s, INP < 200 ms, CLS < 0,1, tamaño de bundle inicial.
- **Navegadores soportados**.
- **Internacionalización**: idiomas, formatos de fecha/moneda, textos externalizados.
- **Sistema de diseño**: librería de componentes, tokens, o "a definir".
- **Privacidad**: qué datos personales se muestran o se guardan en el navegador; analítica y consentimiento de cookies.

## Decisiones típicas del plan
Framework y renderizado (SPA/SSR/SSG), gestión de estado, data fetching y caché, routing, formularios y validación, estilos, estrategia de mocks del backend (p. ej. MSW) para no bloquearse.

## Tareas típicas
1. Esqueleto: app arrancando, una ruta, llamada real o mockeada al backend, desplegable.
2. Layout y navegación.
3. Una tarea por vista o flujo, incluyendo sus estados.
4. Accesibilidad y rendimiento como tareas con verificación propia (axe, Lighthouse), no como "ya se verá".

## Verificación típica
Tests de componente (Testing Library), e2e de flujos críticos (Playwright/Cypress), auditoría axe, Lighthouse con umbrales.
