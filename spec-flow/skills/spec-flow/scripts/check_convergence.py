#!/usr/bin/env python3
"""Verificador mecánico de convergencia entre spec.md y plan.md.

Uso: check_convergence.py <carpeta con spec.md y plan.md>

Errores (exit 1): requisitos sin cubrir, tareas que no cubren nada, IDs inexistentes,
dependencias rotas o circulares, tareas sin verificación o de tamaño L, REQ sin AC,
preguntas [BLOQUEANTE] abiertas, IDs duplicados.
Avisos (no bloquean): NFR sin cifra medible, "Fuera de alcance" vacío.
Si todo está bien imprime el orden de ejecución de las tareas.
"""
from __future__ import annotations

import pathlib
import re
import sys

ID = r"(?:REQ|NFR|AC|T)-\d{3}"
DEF_LINE = re.compile(r"^\s*(?:[-*+]\s+|#{1,6}\s+)\**((?:REQ|NFR|AC)-\d{3})\**(.*)$")
TASK_HEAD = re.compile(r"^#{2,4}\s+(T-\d{3})\b[:\s-]*(.*)$")
SECTION = re.compile(r"^##\s+")


def section(text: str, keyword: str) -> str:
    out, inside = [], False
    for line in text.splitlines():
        if SECTION.match(line):
            inside = keyword.lower() in line.lower()
            continue
        if inside:
            out.append(line)
    return "\n".join(out)


def parse_spec(text: str, errors: list[str], warnings: list[str]):
    defs: dict[str, str] = {}
    ac_to_req: dict[str, list[str]] = {}
    for line in text.splitlines():
        m = DEF_LINE.match(line)
        if not m:
            continue
        ident, rest = m.group(1), m.group(2)
        if ident in defs:
            errors.append(f"{ident} está definido más de una vez en la spec")
        defs[ident] = rest.strip()
        if ident.startswith("AC-"):
            refs = re.findall(r"REQ-\d{3}", rest.split(":")[0])
            ac_to_req[ident] = refs
            if not refs:
                errors.append(f"{ident} no indica a qué requisito pertenece, p. ej. '**{ident}** (REQ-001): ...'")
    for ident, text_ in defs.items():
        if ident.startswith("NFR-") and not re.search(r"\d", text_):
            warnings.append(f"{ident} no contiene ninguna cifra: ¿es medible?")
    blocking = [l.strip() for l in section(text, "preguntas abiertas").splitlines()
                if re.match(r"^\s*[-*]\s+\[ \]\s+\[BLOQUEANTE\]", l, re.I)]
    for b in blocking:
        errors.append(f"Pregunta bloqueante sin resolver: {b[:90]}")
    out_of_scope = [l for l in section(text, "fuera de alcance").splitlines()
                    if re.match(r"^\s*[-*]\s+\S", l) and "<" not in l]
    if not out_of_scope:
        warnings.append("La sección 'Fuera de alcance' está vacía")
    return defs, ac_to_req


def parse_plan(text: str, errors: list[str]):
    tasks: dict[str, dict] = {}
    current = None
    for line in text.splitlines():
        m = TASK_HEAD.match(line)
        if m:
            current = m.group(1)
            if current in tasks:
                errors.append(f"{current} está definida más de una vez en el plan")
            tasks[current] = {"title": m.group(2).strip(), "covers": [], "deps": [],
                              "verif": "", "size": "", "done": False}
            continue
        if SECTION.match(line):
            current = None
            continue
        if not current:
            continue
        t = tasks[current]
        low = line.strip().lower().lstrip("-* ").strip()
        if re.match(r"^\[x\]", low):
            t["done"] = True
        field = low.split(":", 1)
        if len(field) != 2:
            continue
        key, value = field[0].strip("* "), line.split(":", 1)[1].strip()
        if key.startswith("cubre"):
            t["covers"] += re.findall(r"(?:REQ|NFR|AC)-\d{3}", value)
        elif key.startswith("depende"):
            t["deps"] += re.findall(r"T-\d{3}", value)
        elif key.startswith("verificaci"):
            t["verif"] = value
        elif key.startswith("tama"):
            t["size"] = value.upper()[:1]
    return tasks


def topo_order(tasks: dict[str, dict], errors: list[str]) -> list[str]:
    pending = {k: set(d for d in v["deps"] if d in tasks) for k, v in tasks.items()}
    order: list[str] = []
    while pending:
        ready = sorted(k for k, deps in pending.items() if not deps)
        if not ready:
            errors.append("Dependencias circulares entre: " + ", ".join(sorted(pending)))
            break
        for k in ready:
            order.append(k)
            del pending[k]
        for deps in pending.values():
            deps.difference_update(ready)
    return order


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    folder = pathlib.Path(sys.argv[1])
    spec_p, plan_p = folder / "spec.md", folder / "plan.md"
    for p in (spec_p, plan_p):
        if not p.exists():
            print(f"✗ No existe {p}")
            return 2

    errors: list[str] = []
    warnings: list[str] = []
    spec_text = spec_p.read_text(encoding="utf-8")
    plan_text = plan_p.read_text(encoding="utf-8")
    defs, ac_to_req = parse_spec(spec_text, errors, warnings)
    tasks = parse_plan(plan_text, errors)

    reqs = sorted(i for i in defs if i.startswith("REQ-"))
    nfrs = sorted(i for i in defs if i.startswith("NFR-"))
    acs = sorted(i for i in defs if i.startswith("AC-"))
    if not reqs:
        errors.append("La spec no define ningún REQ-NNN")
    if not tasks:
        errors.append("El plan no define ninguna tarea '### T-NNN: título'")

    # Requisitos con criterios de aceptación
    for r in reqs:
        if not any(r in refs for refs in ac_to_req.values()):
            errors.append(f"{r} no tiene ningún criterio de aceptación")
    for ac, refs in ac_to_req.items():
        for r in refs:
            if r not in defs:
                errors.append(f"{ac} apunta a {r}, que no existe en la spec")

    # Cobertura spec -> plan
    covered = {c for t in tasks.values() for c in t["covers"]}
    verified_text = " ".join(t["verif"] for t in tasks.values())
    for i in reqs + nfrs:
        if i not in covered:
            errors.append(f"{i} no está cubierto por ninguna tarea")
    for ac in acs:
        if ac not in covered and ac not in verified_text:
            errors.append(f"{ac} no aparece en 'Cubre' ni en 'Verificación' de ninguna tarea")

    # Calidad de las tareas plan -> spec
    for tid, t in tasks.items():
        if not t["covers"]:
            errors.append(f"{tid} no cubre ningún requisito (¿trabajo que nadie ha pedido?)")
        for c in t["covers"]:
            if c not in defs:
                errors.append(f"{tid} cubre {c}, que no existe en la spec")
        for d in t["deps"]:
            if d not in tasks:
                errors.append(f"{tid} depende de {d}, que no existe")
        if not t["verif"] or t["verif"].startswith("<"):
            errors.append(f"{tid} no tiene verificación concreta")
        if t["size"] == "L":
            errors.append(f"{tid} es de tamaño L: divídela")

    order = topo_order(tasks, errors)

    print(f"Spec: {len(reqs)} REQ · {len(nfrs)} NFR · {len(acs)} AC   Plan: {len(tasks)} tareas "
          f"({sum(t['done'] for t in tasks.values())} hechas)")
    for w in warnings:
        print(f"  ⚠ {w}")
    for e in errors:
        print(f"  ✗ {e}")
    if errors:
        print(f"\n✗ NO CONVERGE: {len(errors)} error(es).")
        return 1
    print("\n✓ CONVERGE. Orden de ejecución:")
    for n, tid in enumerate(order, 1):
        t = tasks[tid]
        mark = "x" if t["done"] else " "
        print(f"  {n:>2}. [{mark}] {tid} {t['title']}  ← {', '.join(t['deps']) or '—'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
