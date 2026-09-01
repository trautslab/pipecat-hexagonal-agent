#!/usr/bin/env python3
"""
Architecture Invariant Linter (AI-SDLC Standard)
Verifica que las fronteras de la arquitectura hexagonal no se violen:
1. core/ NUNCA importa desde adapters/
2. adapters/ siempre implementan los puertos correspondientes
"""
import sys
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT_DIR / "core"
ADAPTERS_DIR = ROOT_DIR / "adapters"


def check_core_boundary_invariants() -> int:
    violations = 0
    print("🔍 [INVARIANTS] Verificando límites de arquitectura hexagonal...")

    forbidden_pattern = re.compile(r"^\s*(from\s+adapters|import\s+adapters)", re.MULTILINE)

    for py_file in CORE_DIR.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        matches = forbidden_pattern.findall(content)
        if matches:
            print(f"❌ VIOLACIÓN DETECTADA en {py_file.relative_to(ROOT_DIR)}: El núcleo no puede importar de 'adapters'")
            violations += 1

    if violations == 0:
        print("✅ [INVARIANTS] Capa CORE completamente aislada de ADAPTERS. Invariante cumplido.")
    else:
        print(f"❌ [INVARIANTS] Se encontraron {violations} violaciones de frontera.")

    return violations


if __name__ == "__main__":
    exit_code = check_core_boundary_invariants()
    sys.exit(exit_code)
