"""Comprueba los enlaces HTTP publicados sin confundir bloqueos con fallos."""

from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[2]
HTML_URL_RE = re.compile(
    r'''(?:href|src)\s*=\s*["'](?P<url>https:''' + r'''//[^"']+)["']'''
)
BARE_URL_RE = re.compile(r"https:" + r"//[^\s'\"<>\x60)}]+")
FALLBACK_TO_GET = {403, 405}
ROBOT_BLOCKS = {401, 403, 429}
USER_AGENT = "Mozilla/5.0 (compatible; notas-a-mano-link-check/1.0)"


def extract_urls(source: str) -> set[str]:
    """Extrae URL completas de HTML, Markdown y texto sin cortar paréntesis."""
    urls: set[str] = set()
    covered: list[tuple[int, int]] = []

    for match in HTML_URL_RE.finditer(source):
        urls.add(html.unescape(match.group("url")).rstrip(".,;:"))
        covered.append(match.span("url"))

    cursor = 0
    while (opening := source.find("](", cursor)) >= 0:
        start = opening + 2
        if not source.startswith("https://", start):
            cursor = start
            continue
        depth = 1
        end = start
        while end < len(source) and depth:
            if source[end] == "(":
                depth += 1
            elif source[end] == ")":
                depth -= 1
            end += 1
        if depth == 0:
            urls.add(html.unescape(source[start : end - 1]).rstrip(".,;:"))
            covered.append((start, end - 1))
        cursor = end

    for match in BARE_URL_RE.finditer(source):
        if any(start <= match.start() < end for start, end in covered):
            continue
        urls.add(html.unescape(match.group()).rstrip(".,;:"))
    return urls


def request_status(url: str, method: str) -> int:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "User-Agent": USER_AGENT,
    }
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request = urllib.request.Request(url, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status
    except HTTPError as error:
        return error.code


def check_url(url: str) -> tuple[str, str]:
    """Retorna ok, blocked o failure junto con su detalle."""
    try:
        status = request_status(url, "HEAD")
        if status in FALLBACK_TO_GET:
            status = request_status(url, "GET")
        if status < 400:
            return "ok", url
        if status in ROBOT_BLOCKS:
            return "blocked", f"HTTP {status}: {url}"
        return "failure", f"HTTP {status}: {url}"
    except Exception as error:
        return "failure", f"{type(error).__name__}: {url} ({error})"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="realiza solicitudes a Internet")
    args = parser.parse_args()
    files = list((ROOT / "docs").rglob("*.md")) + [ROOT / "README.md"]
    urls = sorted({url for path in files for url in extract_urls(path.read_text(encoding="utf-8"))})
    if not args.live:
        print(f"Enlaces publicados inventariados: {len(urls)} (use --live para comprobarlos)")
        return

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check_url, urls))
    failures = [detail for outcome, detail in results if outcome == "failure"]
    blocked = [detail for outcome, detail in results if outcome == "blocked"]
    if blocked:
        print("Enlaces no verificables por políticas antirobot:", file=sys.stderr)
        print("\n".join(blocked), file=sys.stderr)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print(f"Enlaces publicados comprobados: {len(urls) - len(blocked)}; bloqueados por robots: {len(blocked)}")


if __name__ == "__main__":
    main()
