#!/usr/bin/env bash
# Aplica las plantillas de myfactory a un repo existente sin sobrescribir nada.
#   ./scripts/bootstrap-repo.sh /ruta/al/repo
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)/templates"
DEST="$(cd "${1:?Uso: bootstrap-repo.sh /ruta/al/repo}" && pwd)"

put() {  # put <origen relativo a templates> <destino relativo al repo>
  local from="$SRC/$1" to="$DEST/$2"
  if [[ -e "$to" ]]; then echo "  = $2 (ya existe, no se toca)"; return; fi
  mkdir -p "$(dirname "$to")"; cp "$from" "$to"; echo "  + $2"
}

put CLAUDE.md                                   CLAUDE.md
put editorconfig                                .editorconfig
put gitignore                                   .gitignore
put env.example                                 .env.example
put pre-commit-config.yaml                      .pre-commit-config.yaml
put secretsignore                               .secretsignore
put github/pull_request_template.md             .github/pull_request_template.md
put github/ISSUE_TEMPLATE/bug_report.md         .github/ISSUE_TEMPLATE/bug_report.md
put github/ISSUE_TEMPLATE/feature_request.md    .github/ISSUE_TEMPLATE/feature_request.md
put docs/adr-template.md                        docs/adr/0000-plantilla.md

# Hook de git local que ejecuta secrets-guard antes de cada commit
if [[ -d "$DEST/.git" && ! -e "$DEST/.git/hooks/pre-commit" ]]; then
  SCANNER="$(cd "$SRC/.." && pwd)/skills/secrets-guard/scripts/scan_secrets.py"
  printf '#!/usr/bin/env bash\npython3 "%s" --staged\n' "$SCANNER" > "$DEST/.git/hooks/pre-commit"
  chmod +x "$DEST/.git/hooks/pre-commit"
  echo "  + .git/hooks/pre-commit (secrets-guard)"
fi
echo "✓ Bootstrap completado en $DEST. Revisa y personaliza CLAUDE.md."
