from __future__ import annotations

import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".md", ".tex", ".py", ".ipynb"}
COLAB_LINK_RE = re.compile(
    r"https://colab\.research\.google\.com/github/"
    r"Notas-a-Mano-serie-de-libros/"
    r"3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
    r"blob/main/(?P<path>[^\\s)\\]}\"']+?\.ipynb)"
)


def iter_text_files():
    ignored_parts = {".git", ".pytest_cache", "__pycache__"}
    for path in sorted(PROJECT_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if ignored_parts.intersection(path.parts):
            continue
        if path.suffix in TEXT_EXTENSIONS:
            yield path


def validate_links() -> list[str]:
    errors = []
    found = 0
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        for match in COLAB_LINK_RE.finditer(text):
            found += 1
            notebook_path = PROJECT_ROOT / match.group("path")
            if not notebook_path.exists():
                errors.append(
                    f"{path.relative_to(PROJECT_ROOT)} referencia un notebook inexistente: "
                    f"{notebook_path.relative_to(PROJECT_ROOT)}"
                )

    return errors


def main() -> None:
    errors = validate_links()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)

    print("Enlaces de GitHubColab validados cuando están presentes.")


if __name__ == "__main__":
    main()
