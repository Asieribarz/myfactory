#!/usr/bin/env python3
"""secrets-guard: escáner ligero de secretos y datos personales (PII).

Uso:
  scan_secrets.py [--staged] [--no-pii] [rutas...]

Sin rutas: escanea los ficheros versionados por git (o el directorio actual).
--staged: escanea solo las líneas añadidas en staging (ideal para pre-commit).
Sale con código 1 si encuentra algo. Nunca imprime los valores completos.
"""
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys

DUMMY_MARKERS = (
    "test", "dummy", "example", "ejemplo", "sample", "fake", "changeme",
    "placeholder", "xxxx", "1234", "your_", "tu_", "<", "${", "{{", "redacted",
)
IGNORE_INLINE = "secrets-guard: ignore"
BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz",
    ".tar", ".jar", ".exe", ".dll", ".so", ".dylib", ".woff", ".woff2", ".ttf",
    ".mp4", ".mp3", ".lock",
}

SECRET_RULES = [
    ("Clave privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("AWS Access Key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("Anthropic/OpenAI key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_\-]{20,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Stripe key", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{20,}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")),
    ("Bearer token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9_\-\.=]{20,}")),
    ("Cadena de conexión", re.compile(
        r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp|mssql)://[^\s:@/]+:[^\s@/]+@[^\s]+"
        r"|\b(?:Password|Pwd)\s*=\s*[^;\s]{4,};")),
    ("Azure Tenant/Client ID", re.compile(
        r"(?i)(?:tenant|client|app)[_\- ]?id['\"]?\s*[:=]\s*['\"]?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")),
    ("Asignación de secreto", re.compile(
        r"(?i)\b(?:api[_\-]?key|secret|password|passwd|pwd|token|access[_\-]?key|private[_\-]?key|client[_\-]?secret)"
        r"['\"]?\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]")),
]

PII_RULES = [
    ("Email", re.compile(r"(?<![\w.%+\-:/])[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("DNI/NIE", re.compile(r"\b[XYZ]?\d{7,8}[-\s]?[A-Z]\b")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[0-9A-Z]{4}){4,7}\b")),
    ("Teléfono ES", re.compile(r"(?<![\d.])(?:\+34[\s\-]?)?[6789]\d{2}[\s\-]?\d{3}[\s\-]?\d{3}(?![\d.])")),
]
SAFE_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "test.com", "localhost",
                      "users.noreply.github.com", "noreply.github.com")
DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


def valid_dni(raw: str) -> bool:
    s = re.sub(r"[-\s]", "", raw.upper())
    s = s.replace("X", "0", 1) if s.startswith("X") else s
    s = s.replace("Y", "1", 1) if s.startswith("Y") else s
    s = s.replace("Z", "2", 1) if s.startswith("Z") else s
    if not re.fullmatch(r"\d{8}[A-Z]", s):
        return False
    return DNI_LETTERS[int(s[:8]) % 23] == s[8]


def valid_iban(raw: str) -> bool:
    s = raw.replace(" ", "")
    if len(s) < 15:
        return False
    rearranged = s[4:] + s[:4]
    digits = "".join(str(int(c, 36)) for c in rearranged)
    return int(digits) % 97 == 1


def is_dummy(value: str) -> bool:
    low = value.lower()
    return any(m in low for m in DUMMY_MARKERS)


def mask(value: str) -> str:
    v = value.strip()
    if len(v) <= 6:
        return "***"
    return f"{v[:3]}…{v[-2:]} ({len(v)} car.)"


def load_ignore_globs() -> list[str]:
    if not os.path.exists(".secretsignore"):
        return []
    with open(".secretsignore", encoding="utf-8") as fh:
        return [l.strip() for l in fh if l.strip() and not l.startswith("#")]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout


def iter_targets(paths: list[str]):
    if paths:
        for p in paths:
            if os.path.isdir(p):
                for root, dirs, files in os.walk(p):
                    dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "venv", "dist", "build"}]
                    for f in files:
                        yield os.path.join(root, f)
            else:
                yield p
        return
    listed = git("ls-files").splitlines()
    if listed:
        yield from listed
    else:
        yield from iter_targets(["."])


def staged_lines():
    """Devuelve (fichero, nº línea, texto) de las líneas añadidas en staging."""
    diff = git("diff", "--cached", "--unified=0", "--no-color")
    current, lineno = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
        elif line.startswith("+") and current:
            yield current, lineno, line[1:]
            lineno += 1


def file_lines(path: str):
    if os.path.splitext(path)[1].lower() in BINARY_EXT:
        return
    try:
        if os.path.getsize(path) > 2_000_000:
            return
        with open(path, encoding="utf-8", errors="strict") as fh:
            for i, line in enumerate(fh, 1):
                yield path, i, line.rstrip("\n")
    except (UnicodeDecodeError, OSError):
        return


def scan_line(text: str, check_pii: bool):
    if IGNORE_INLINE in text:
        return
    for label, rx in SECRET_RULES:
        for m in rx.finditer(text):
            value = m.group(m.lastindex or 0)
            if not is_dummy(value):
                yield "SECRETO", label, value
    if not check_pii:
        return
    for label, rx in PII_RULES:
        for m in rx.finditer(text):
            value = m.group(0)
            if is_dummy(value):
                continue
            if label == "Email" and value.lower().split("@")[-1].endswith(SAFE_EMAIL_DOMAINS):
                continue
            if label == "DNI/NIE" and not valid_dni(value):
                continue
            if label == "IBAN" and not valid_iban(value):
                continue
            yield "PII", label, value


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--staged", action="store_true", help="escanear solo líneas añadidas en staging")
    ap.add_argument("--no-pii", action="store_true", help="no buscar datos personales")
    args = ap.parse_args()

    ignore = load_ignore_globs() + [".secretsignore", "*scan_secrets.py"]
    lines = staged_lines() if args.staged else (
        l for p in iter_targets(args.paths) for l in file_lines(p))

    findings = 0
    for path, lineno, text in lines:
        if any(fnmatch.fnmatch(path, g) for g in ignore):
            continue
        for kind, label, value in scan_line(text, not args.no_pii):
            findings += 1
            print(f"[{kind}] {path}:{lineno}  {label}: {mask(value)}")

    if findings:
        print(f"\n✗ {findings} posible(s) hallazgo(s). Revisa, sustituye por variables de entorno/placeholders "
              "y rota cualquier credencial expuesta.", file=sys.stderr)
        return 1
    print("✓ Sin secretos ni datos personales detectados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
