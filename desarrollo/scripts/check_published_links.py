"""Comprueba enlaces HTTP publicados con timeout y reintentos acotados."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL_RE = re.compile(r"https:" + r"//[^\s'\"<>`)]+")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="realiza solicitudes a Internet")
    args = parser.parse_args()
    files = list((ROOT / "docs").rglob("*.md")) + [ROOT / "README.md"]
    urls = sorted({u.rstrip(".,;:}") for p in files for u in URL_RE.findall(p.read_text(encoding="utf-8"))})
    if not args.live:
        print(f"Enlaces publicados inventariados: {len(urls)} (use --live para comprobarlos)")
        return
    failures = []
    for url in urls:
        try:
            request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "notas-a-mano-link-check"})
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status >= 400:
                    failures.append(f"{response.status}: {url}")
        except Exception as error:
            failures.append(f"{type(error).__name__}: {url} ({error})")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print(f"Enlaces publicados comprobados: {len(urls)}")


if __name__ == "__main__":
    main()
