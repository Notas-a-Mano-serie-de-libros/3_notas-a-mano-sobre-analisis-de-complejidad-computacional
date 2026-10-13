"""Prueba funcional y de accesibilidad básica del portal (Playwright).

Verifica en 375 px y 1280 px que las páginas clave no tengan scroll
horizontal, LaTeX sin renderizar, estructura, nombres accesibles y teclado.

Uso: python desarrollo/scripts/smoke_portal_e2e.py --site-dir site
Requiere: pip install playwright && playwright install chromium
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import sys
import threading
from pathlib import Path

PAGES = (
    "",
    "capitulos/capitulo-2/",
    "capitulos/capitulo-5/ecuacion-caracteristica/",
    "capitulos/capitulo-6/merge-sort/",
    "capitulos/capitulo-8/",
)
VIEWPORTS = ((375, 800), (1280, 900))
HEADING_JS = "[...document.querySelectorAll('.md-content h1,.md-content h2,.md-content h3,.md-content h4,.md-content h5,.md-content h6')].map(h=>+h.tagName[1])"


def serve(site_dir: Path):
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass

    handler = functools.partial(QuietHandler, directory=str(site_dir))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def check_page(page, url: str, width: int) -> list[str]:
    problems = []
    page.goto(url, wait_until="load")
    page.wait_for_timeout(500)
    if page.evaluate("document.documentElement.scrollWidth") > width:
        problems.append(f"scroll horizontal a {width}px")
    text = page.evaluate("document.querySelector('.md-content').innerText")
    if re.search(r"\\\(|\\\[|\$\$", text):
        problems.append("LaTeX sin renderizar")
    levels = page.evaluate(HEADING_JS)
    if any(b - a > 1 for a, b in zip(levels, levels[1:], strict=False)):
        problems.append(f"salto de encabezados {levels}")
    unnamed = page.evaluate(
        """[...document.querySelectorAll('button,a[href],input,select,textarea,iframe')]
        .filter(el => !el.disabled && !el.hidden && el.type !== 'hidden')
        .filter(el => !(el.textContent.trim() || el.getAttribute('aria-label') ||
          el.getAttribute('aria-labelledby') || el.getAttribute('title') ||
          (el.labels && el.labels.length)))
        .map(el => el.outerHTML.slice(0, 160))"""
    )
    if unnamed:
        problems.append(f"controles sin nombre accesible: {unnamed[:3]}")
    page.keyboard.press("Tab")
    focus = page.evaluate(
        """(() => { const el=document.activeElement; const s=getComputedStyle(el);
        return {tag:el?.tagName, outline:s.outlineStyle, width:s.outlineWidth}; })()"""
    )
    if not focus["tag"] or (focus["outline"] == "none" and focus["width"] == "0px"):
        problems.append("el primer control de teclado no muestra foco visible")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", default="site")
    args = parser.parse_args()
    from playwright.sync_api import sync_playwright

    server = serve(Path(args.site_dir))
    host, port = server.server_address[:2]
    base = "".join(("http", "://", host, ":", str(port), "/"))
    failures = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for width, height in VIEWPORTS:
            page = browser.new_page(
                viewport={"width": width, "height": height},
                reduced_motion="reduce",
            )
            for path in PAGES:
                for problem in check_page(page, base + path, width):
                    failures.append(f"{path or '/'} @{width}: {problem}")
            page.close()
        zoom_page = browser.new_page(viewport={"width": 1280, "height": 900})
        zoom_page.goto(base, wait_until="load")
        zoom_page.evaluate("document.documentElement.style.zoom='200%'")
        if zoom_page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth"):
            failures.append("/ @zoom-200: scroll horizontal")
        zoom_page.close()
        browser.close()
    server.shutdown()
    for failure in failures:
        print("FALLO", failure)
    print(f"{len(PAGES) * len(VIEWPORTS)} comprobaciones; {len(failures)} fallos.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
