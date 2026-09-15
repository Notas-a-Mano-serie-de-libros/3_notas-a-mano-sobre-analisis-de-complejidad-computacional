"""Mantiene las instrucciones locales junto a cada enlace de simulación en Pages."""

from __future__ import annotations

import argparse
import json
import re
import shlex
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
START = "<!-- local-execution:start -->"
END = "<!-- local-execution:end -->"
NOTEBOOK_LINK = re.compile(
    r"https://(?:colab\.research\.google\.com/github|githubtocolab\.com)/"
    r"Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
    r"blob/main/(simulaciones/capitulo[2-8]/notebooks/[^\s\"'<>]*?\.ipynb)"
)


def simulation_paths(content: str) -> list[str]:
    return list(dict.fromkeys(unquote(match).replace("\\", "") for match in NOTEBOOK_LINK.findall(content)))


def simulation_title(path: str) -> str:
    notebook = json.loads((ROOT / path).read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        match = re.search(r"^#+\s+(.+)", "".join(cell.get("source", [])), flags=re.MULTILINE)
        if match:
            title = match.group(1).split(" · ")[0]
            return re.sub(r"^Ejemplo \d+:\s*", "", title)
    return Path(path).stem.replace("_", " ")


def local_section(paths: list[str]) -> str:
    chapters = list(dict.fromkeys(Path(path).parts[1] for path in paths))
    chapter_laboratory = all(chapter in {"capitulo7", "capitulo8"} for chapter in chapters)
    rows = []
    for chapter in chapters if chapter_laboratory else []:
        rows.append(f"| Abrir el laboratorio del capítulo {chapter.removeprefix('capitulo')} | `jupyter lab simulaciones/{chapter}/notebooks/` |")
    for path in [] if chapter_laboratory else paths:
        title = re.sub(r"\$(.+?)\$", lambda m: r"\(" + m.group(1) + r"\)", simulation_title(path))
        rows.append(f"| Abrir {title} | `jupyter lab {shlex.quote(path)}` |")
    return "\n".join([
        START,
        '<details class="local-execution" markdown="1">',
        "<summary>Recomendación de ejecución local</summary>",
        "",
        "Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno "
        "según la [guía de instalación]"
        "(https://github.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) "
        + ("y abra la carpeta de notebooks del capítulo con Jupyter Lab:" if chapter_laboratory
           else "y ejecute el notebook con Jupyter:"),
        "",
        "| Paso | Comando |",
        "| --- | --- |",
        "| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |",
        *rows,
        "",
        ("Jupyter Lab abrirá la carpeta; elija una simulación y ejecute todas sus celdas." if chapter_laboratory
         else "Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla."),
        "",
        "La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.",
        "</details>",
        END,
    ])


def update_content(content: str) -> str:
    content = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n*", "", content, flags=re.DOTALL)
    # Sustituir las cuatro recomendaciones anteriores por el formato común.
    content = re.sub(
        r"^#{2,3} Recomendación de ejecución local\s*\n.*?(?=^#{1,6} |^<nav |^---\s*$|\Z)",
        "", content, flags=re.MULTILINE | re.DOTALL,
    )
    paths = simulation_paths(content)
    if not paths:
        return content
    section = local_section(paths)
    # Mantener las instrucciones dentro del contenido y antes de los cierres editoriales.
    boundary = re.search(
        r'^!!! \w+ "Para cerrar la lectura"|^<nav class="(?:section-return|chapter-nav chapter-nav--bottom)', content, flags=re.MULTILINE,
    )
    offset = boundary.start() if boundary else len(content.rstrip())
    updated = content[:offset].rstrip() + "\n\n" + section + "\n\n" + content[offset:].lstrip()
    return updated.rstrip() + "\n"


def sync(check: bool = False) -> list[Path]:
    changed = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        content = path.read_text(encoding="utf-8")
        if not simulation_paths(content) and START not in content:
            continue
        updated = update_content(content)
        if updated != content:
            changed.append(path)
            if not check:
                path.write_text(updated, encoding="utf-8")
    return changed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = sync(check=args.check)
    if args.check and changed:
        for path in changed:
            print(f"Instrucciones locales desactualizadas: {path.relative_to(ROOT)}")
        raise SystemExit(1)
    print("Instrucciones de ejecución local sincronizadas en Pages.")
