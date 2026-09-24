#!/usr/bin/env python3
"""Hook PreToolUse de Claude Code: bloquea `git commit` si hay secretos en staging.

Recibe por stdin el JSON de la llamada a la herramienta. Si el comando contiene
`git commit`, ejecuta secrets-guard en modo --staged --no-pii. Exit 2 = bloquear
(el mensaje de stderr se devuelve a Claude para que lo corrija).
"""
import json
import os
import subprocess
import sys

try:
    payload = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

command = (payload.get("tool_input") or {}).get("command", "")
if "git commit" not in command:
    sys.exit(0)

root = os.environ.get("CLAUDE_PLUGIN_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
scanner = os.path.join(root, "skills", "secrets-guard", "scripts", "scan_secrets.py")
result = subprocess.run([sys.executable, scanner, "--staged", "--no-pii"], capture_output=True, text=True)

if result.returncode == 1:
    sys.stderr.write("Commit bloqueado por secrets-guard: posibles secretos en staging.\n"
                     + result.stdout + "Sustitúyelos por variables de entorno/placeholders y vuelve a intentarlo.\n")
    sys.exit(2)
sys.exit(0)
