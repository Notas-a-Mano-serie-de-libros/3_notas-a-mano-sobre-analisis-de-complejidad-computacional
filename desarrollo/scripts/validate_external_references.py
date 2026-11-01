"""Valida que las referencias externas del proyecto sean explícitas y seguras."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
URL_RE = re.compile(r"https?" + r"://[^\s'\"<>`)]+")
SKIP = {
    ".git",
    ".venv",
    "site",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".ipynb_checkpoints",
    ".virtual_documents",
}


def validate(root: Path = ROOT) -> tuple[list[str], int]:
    errors: list[str] = []
    urls = 0
    for current, directories, names in os.walk(root):
        directories[:] = [name for name in directories if name not in SKIP]
        for name in names:
            path = Path(current) / name
            if path.suffix not in {".py", ".md", ".yml", ".yaml", ".json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for raw in URL_RE.findall(text):
                url = raw.rstrip(".,;:}")
                urls += 1
                try:
                    parsed = urlparse(url)
                    hostname = parsed.hostname
                except ValueError:
                    errors.append(f"{path.relative_to(root)}: URL malformada: {url}")
                    continue
                if parsed.scheme != "https":
                    errors.append(f"{path.relative_to(root)}: URL no segura: {url}")
                if hostname in {"localhost", "127.0.0.1", "0.0.0.0"}:
                    errors.append(f"{path.relative_to(root)}: URL local publicada: {url}")
    return errors, urls


def main() -> int:
    errors, urls = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Referencias externas válidas: {urls}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
