"""Valida que las referencias externas del proyecto sean explícitas y seguras."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
URL_RE = re.compile(r"https?" + r"://[^\s'\"<>`)]+")
SKIP = {".git", ".venv", "site", "__pycache__", ".pytest_cache", ".ruff_cache"}


def main() -> None:
    errors: list[str] = []
    urls = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or SKIP.intersection(path.parts):
            continue
        if path.suffix not in {".py", ".md", ".yml", ".yaml", ".json"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for raw in URL_RE.findall(text):
            url = raw.rstrip(".,;:}")
            urls += 1
            parsed = urlparse(url)
            if parsed.scheme != "https":
                errors.append(f"{path.relative_to(ROOT)}: URL no segura: {url}")
            if parsed.hostname in {"localhost", "127.0.0.1", "0.0.0.0"}:
                errors.append(f"{path.relative_to(ROOT)}: URL local publicada: {url}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Referencias externas válidas: {urls}")


if __name__ == "__main__":
    main()
