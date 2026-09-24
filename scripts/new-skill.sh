#!/usr/bin/env bash
# Crea el esqueleto de una skill nueva: ./scripts/new-skill.sh nombre-en-kebab
set -euo pipefail
NAME="${1:?Uso: new-skill.sh nombre-en-kebab}"
DIR="$(cd "$(dirname "$0")/.." && pwd)/skills/$NAME"
[[ -e "$DIR" ]] && { echo "Ya existe $DIR"; exit 1; }
mkdir -p "$DIR"
cat > "$DIR/SKILL.md" <<SKILL
---
name: $NAME
description: QUÉ hace y CUÁNDO usarla. Incluye frases que diría el usuario ("...", "...") para que se active bien.
---

# ${NAME}

## Proceso
1. ...

## Formato de salida
...
SKILL
echo "✓ Creada $DIR/SKILL.md"
