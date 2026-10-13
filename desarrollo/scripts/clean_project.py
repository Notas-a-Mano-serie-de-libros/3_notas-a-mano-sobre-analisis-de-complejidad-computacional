"""Elimina artefactos locales regenerables sin tocar fuentes del proyecto."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATED = {"site", ".pytest_cache", ".ruff_cache", ".mypy_cache", "__pycache__", ".ipynb_checkpoints", ".virtual_documents"}


def main() -> None:
    removed: list[str] = []
    for path in sorted(ROOT.rglob("*"), reverse=True):
        if not path.is_dir() or path.name not in GENERATED or path == ROOT / ".venv":
            continue
        shutil.rmtree(path)
        removed.append(str(path.relative_to(ROOT)))
    print(f"Artefactos eliminados: {len(removed)}")
    for path in removed:
        print(path)


if __name__ == "__main__":
    main()
