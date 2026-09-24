#!/usr/bin/env bash
# Instala las skills (y agentes/comandos) de myfactory sin usar el sistema de plugins.
#   ./scripts/install.sh              -> global (~/.claude)
#   ./scripts/install.sh /ruta/repo   -> solo en ese repo (<repo>/.claude)
#   ./scripts/install.sh --link ...   -> symlinks en vez de copias (se actualizan con git pull)
set -euo pipefail

MODE=copy
if [[ "${1:-}" == "--link" ]]; then MODE=link; shift; fi

SRC="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -ge 1 ]]; then DEST="$(cd "$1" && pwd)/.claude"; else DEST="$HOME/.claude"; fi

for kind in skills agents commands; do
  [[ -d "$SRC/$kind" ]] || continue
  mkdir -p "$DEST/$kind"
  for item in "$SRC/$kind"/*; do
    name="$(basename "$item")"
    target="$DEST/$kind/$name"
    rm -rf "$target"
    if [[ $MODE == link ]]; then ln -s "$item" "$target"; else cp -R "$item" "$target"; fi
    echo "  $kind/$name -> $target"
  done
done
echo "✓ myfactory instalado en $DEST ($MODE)"
