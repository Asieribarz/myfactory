---
name: changelog
description: Genera o actualiza CHANGELOG.md y notas de release a partir del historial git, siguiendo Keep a Changelog y SemVer. Úsala cuando el usuario diga "prepara la release", "actualiza el changelog", "¿qué ha cambiado desde la última versión?" o "release notes".
---

# Changelog y releases

1. Última versión: `git describe --tags --abbrev=0` (si no hay tags, desde el primer commit).
2. Commits: `git log <tag>..HEAD --pretty=format:'%s%n%b' --no-merges`.
3. Clasifica (según Conventional Commits si se usan):
   - `feat` → **Added**; `fix` → **Fixed**; `perf`/`refactor` visibles → **Changed**; eliminaciones → **Removed**; seguridad → **Security**; `BREAKING CHANGE` → destacarlo arriba.
   - Omite `chore`, `ci`, `style`, `test` salvo que afecten al usuario.
4. Propón la siguiente versión SemVer: breaking → MAJOR, feat → MINOR, solo fixes → PATCH.
5. Añade la sección al principio de `CHANGELOG.md` (créalo si no existe) con formato Keep a Changelog.
6. Redacta en lenguaje de usuario, no de commit. Sin nombres de personas ni datos personales.
