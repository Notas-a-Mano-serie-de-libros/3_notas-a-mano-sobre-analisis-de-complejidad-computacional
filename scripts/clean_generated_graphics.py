from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KEEP_FILE = ".gitkeep"


def graphics_roots() -> list[Path]:
    return sorted(PROJECT_ROOT.glob("capitulo[0-9]*/images/generadas"))


def generated_graphics() -> list[Path]:
    files: list[Path] = []
    for graphics_root in graphics_roots():
        files.extend(
            path
            for path in graphics_root.rglob("*")
            if path.is_file() and path.name not in {KEEP_FILE, "README.md"}
        )
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Elimina las imágenes generadas dentro de images/generadas de cada capítulo."
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
