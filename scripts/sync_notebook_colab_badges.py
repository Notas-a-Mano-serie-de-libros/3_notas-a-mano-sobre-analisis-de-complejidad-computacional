"""Añade a los notebooks enlazados desde los README su acceso directo a Colab."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = (
    "Notas-a-Mano-serie-de-libros/"
    "3_notas-a-mano-sobre-analisis-de-complejidad-computacional"
)


def badge(relative_path: Path) -> str:
    url = f"https://colab.research.google.com/github/{REPOSITORY}/blob/main/{relative_path.as_posix()}"
    return (
        "[![Abrir en Google Colab]"
        "(https://colab.research.google.com/assets/colab-badge.svg)]"
        f"({url})"
    )


def linked_notebooks() -> list[Path]:
    return sorted(
        path
        for chapter in range(2, 9)
        for path in (ROOT / f"capitulo{chapter}" / "notebooks").glob("*.ipynb")
    )


def update_notebook(path: Path) -> bool:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    relative_path = path.relative_to(ROOT)
    marker = "Abrir en Google Colab"
    if marker in json.dumps(notebook, ensure_ascii=False):
        return False

    markdown = next(
        (cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "markdown"),
        None,
    )
    if markdown is None:
        markdown = {
            "cell_type": "markdown",
            "id": "colab-access",
            "metadata": {},
            "source": [badge(relative_path) + "\n"],
        }
        notebook.setdefault("cells", []).insert(0, markdown)
    else:
        source = markdown.setdefault("source", [])
        if source and not source[-1].endswith("\n"):
            source[-1] += "\n"
        source.extend(["\n", badge(relative_path) + "\n"])

    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    return True


def main() -> None:
    paths = linked_notebooks()
    updated = sum(update_notebook(path) for path in paths)
    print(f"Badges de Colab: {updated} actualizados, {len(paths)} verificados.")


if __name__ == "__main__":
    main()
