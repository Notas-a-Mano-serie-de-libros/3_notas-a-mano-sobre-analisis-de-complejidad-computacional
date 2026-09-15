"""Reconstruye los recursos publicados de Pages desde sus fuentes del libro."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from desarrollo.scripts.image_assets import published_bytes
except ModuleNotFoundError:
    from image_assets import published_bytes

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "desarrollo/scripts/data/page_asset_sources.json"


def sync(check: bool = False) -> list[str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    for destination_name, source_name in manifest.items():
        destination = ROOT / destination_name
        source = ROOT / source_name
        if not source.is_file():
            errors.append(f"Fuente ausente: {source_name}")
            continue
        expected = published_bytes(source)
        if check:
            if not destination.is_file() or destination.read_bytes() != expected:
                errors.append(f"Recurso desactualizado: {destination_name}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(expected)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = sync(check=args.check)
    if errors:
        print("\n".join(errors))
        return 1
    print("Recursos de Pages sincronizados desde las fuentes del libro.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
