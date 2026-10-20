"""Genera la bibliografía web desde el archivo BibTeX canónico de la obra."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "desarrollo/scripts/data/referencias.bib"
TARGET = ROOT / "docs/bibliografia.md"


def entries(source: str) -> list[str]:
    result: list[str] = []
    start = None
    depth = 0
    for index, character in enumerate(source):
        if start is None:
            if character == "@" and (index == 0 or source[index - 1] == "\n"):
                start = index
                depth = 0
            continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                result.append(source[start : index + 1])
                start = None
    return result


def field(entry: str, name: str) -> str:
    match = re.search(
        rf"(?mis)^\s*{re.escape(name)}\s*=\s*\{{((?:[^{{}}]|\{{[^{{}}]*\}})*)\}}\s*,?",
        entry,
    )
    if match:
        return clean(match.group(1))
    bare = re.search(
        rf"(?mi)^\s*{re.escape(name)}\s*=\s*([^\n,]+)\s*,?",
        entry,
    )
    return clean(bare.group(1).strip().strip('{}\"')) if bare else ""


def clean(value: str) -> str:
    replacements = {
        r"\'a": "á", r"\'e": "é", r"\'i": "í", r"\'o": "ó", r"\'u": "ú",
        r"\'A": "Á", r"\'E": "É", r"\'I": "Í", r"\'O": "Ó", r"\'U": "Ú",
        r'\"a': "ä", r'\"o': "ö", r'\"u': "ü", r"\~n": "ñ", r"\&": "&",
        "{": "", "}": "", "\\textit": "", "\\textbf": "", "\n": " ",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return re.sub(r"\s+", " ", value).strip()


def render(entry: str) -> tuple[str, str]:
    key_match = re.match(r"@\w+\{([^,]+)", entry)
    key = key_match.group(1) if key_match else "referencia"
    author = field(entry, "author") or field(entry, "editor") or "Autor no indicado"
    author = author.replace(" and ", "; ")
    if author == "ISO":
        author = "International Organization for Standardization"
    year = field(entry, "year") or "s. f."
    title = field(entry, "title") or key
    container = (
        field(entry, "journal")
        or field(entry, "booktitle")
        or field(entry, "publisher")
        or field(entry, "institution")
        or field(entry, "organization")
    )
    doi = field(entry, "doi")
    url = field(entry, "url")
    if url.startswith("http://"):
        url = "https://" + url.removeprefix("http://")
    destination = f"https://doi.org/{doi}" if doi else url
    title_text = f"[{title}]({destination})" if destination else title
    suffix = f" *{container}*." if container else ""
    return f"{author.lower()} {year} {title.lower()}", f"- {author} ({year}). {title_text}.{suffix}"


def build() -> str:
    rendered = sorted(render(entry) for entry in entries(SOURCE.read_text(encoding="utf-8")))
    lines = [
        "# Bibliografía de la obra",
        "",
        "Esta página reúne las referencias del manuscrito que sustenta la edición web. "
        "Los DOI y enlaces disponibles conducen a la fuente original; su inclusión no "
        "implica que el recurso sea de acceso abierto.",
        "",
        f"**Total de referencias:** {len(rendered)}.",
        "",
        *[line for _, line in rendered],
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        if not TARGET.is_file() or TARGET.read_text(encoding="utf-8") != expected:
            print("La bibliografía web no está sincronizada; ejecute este script sin --check.")
            return 1
        print("Bibliografía web sincronizada con referencias.bib.")
        return 0
    TARGET.write_text(expected, encoding="utf-8")
    print(f"Bibliografía web generada: {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
