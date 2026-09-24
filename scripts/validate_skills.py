#!/usr/bin/env python3
"""Valida que cada skills/*/SKILL.md tenga frontmatter con name y description correctos."""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []
for skill in sorted(root.glob("**/skills/*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{skill}: falta frontmatter YAML"); continue
    fields = dict(re.findall(r"^([\w-]+):\s*(.+)$", m.group(1), re.M))
    folder = skill.parent.name
    if fields.get("name") != folder:
        errors.append(f"{skill}: name '{fields.get('name')}' debe coincidir con la carpeta '{folder}'")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", fields.get("name", "")):
        errors.append(f"{skill}: name debe ser kebab-case (≤64)")
    desc = fields.get("description", "")
    if len(desc) < 40 or len(desc) > 1024:
        errors.append(f"{skill}: description debe tener entre 40 y 1024 caracteres")
    if len(text.splitlines()) > 500:
        errors.append(f"{skill}: más de 500 líneas; mueve detalle a references/")
    print(f"{'✓' if not any(str(skill) in e for e in errors) else '✗'} {folder}")

for e in errors:
    print("ERROR:", e, file=sys.stderr)
sys.exit(1 if errors else 0)
