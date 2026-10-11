"""Sincroniza las incrustaciones con los perfiles del catálogo JupyterLite."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from desarrollo.scripts.jupyterlite_catalog import (
        PAGE_NOTEBOOKS,
        profile_for_chapter,
    )
except ModuleNotFoundError:
    from jupyterlite_catalog import PAGE_NOTEBOOKS, profile_for_chapter


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def notebook_url(chapter: int, notebook: Path) -> str:
    profile = profile_for_chapter(chapter)
    encoded_path = str(notebook).replace("/", "%2F")
    return f"jupyterlite/{profile}/notebooks/index.html?path={encoded_path}"


def synchronize(check: bool = False) -> list[Path]:
    changed = []
    errors = []
    for (chapter, page), notebooks in PAGE_NOTEBOOKS.items():
        path = DOCS / "capitulos" / f"capitulo-{chapter}" / f"{page}.md"
        if not path.is_file():
            errors.append(f"Falta la página catalogada: {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8")
        updated = content
        for notebook in notebooks:
            target = notebook_url(chapter, notebook)
            previous = f"jupyterlite/capitulo-{chapter}/notebooks/index.html?path={str(notebook).replace('/', '%2F')}"
            if previous in updated:
                updated = updated.replace(previous, target)
            elif target not in updated:
                errors.append(
                    f"{path.relative_to(ROOT)}: no se encontró la incrustación de {notebook}"
                )
        if updated != content:
            changed.append(path)
            if not check:
                path.write_text(updated, encoding="utf-8")
    if errors:
        raise ValueError("\n".join(errors))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = synchronize(check=args.check)
    if args.check and changed:
        for path in changed:
            print(f"URL JupyterLite desactualizada: {path.relative_to(ROOT)}")
        return 1
    print("URLs JupyterLite sincronizadas con el catálogo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
