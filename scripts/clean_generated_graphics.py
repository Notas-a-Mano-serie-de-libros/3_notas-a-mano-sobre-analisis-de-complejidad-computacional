from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KEEP_FILE = ".gitkeep"


def generated_graphics() -> list[Path]:
    files: list[Path] = []
    for graphics_dir in PROJECT_ROOT.rglob("graficas"):
        if not graphics_dir.is_dir() or ".git" in graphics_dir.parts:
            continue
        files.extend(
            path
            for path in graphics_dir.rglob("*")
            if path.is_file() and path.name != KEEP_FILE
        )
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Elimina las imágenes generadas dentro de carpetas graficas/."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Solo verifica; falla si encuentra resultados generados.",
    )
    args = parser.parse_args()
    files = generated_graphics()

    for path in files:
        print(path.relative_to(PROJECT_ROOT))
        if not args.check:
            path.unlink()

    return 1 if args.check and files else 0


if __name__ == "__main__":
    raise SystemExit(main())
