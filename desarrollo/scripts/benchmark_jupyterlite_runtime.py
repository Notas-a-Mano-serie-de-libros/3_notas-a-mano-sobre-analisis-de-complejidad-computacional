"""Mide la apertura real de cada perfil JupyterLite en Chromium."""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import threading
import time
from pathlib import Path
from urllib.parse import quote

try:
    from desarrollo.scripts.jupyterlite_catalog import PROFILE_CONFIGS
except ModuleNotFoundError:
    from jupyterlite_catalog import PROFILE_CONFIGS

ROOT = Path(__file__).resolve().parents[2]
MAX_NOTEBOOK_READY_MS = 45_000
MAX_REQUESTS = 400


def serve(site_dir: Path):
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass

    class Server(http.server.ThreadingHTTPServer):
        # La cola por defecto (5) reinicia conexiones al cargar decenas de chunks en paralelo.
        request_queue_size = 128

    handler = functools.partial(QuietHandler, directory=str(site_dir))
    server = Server(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def measure(browser, base: str, profile: str, notebook: Path | str) -> dict[str, object]:
    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    requests = 0
    failures: list[str] = []
    def count_request(_request) -> None:
        nonlocal requests
        requests += 1

    page.on("request", count_request)
    page.on("requestfailed", lambda request: failures.append(request.url))
    notebook = Path(notebook).as_posix()
    url = f"{base}{profile}/notebooks/index.html?path={quote(notebook, safe='')}"
    start = time.perf_counter()
    page.goto(url, wait_until="domcontentloaded", timeout=MAX_NOTEBOOK_READY_MS)
    page.locator(".jp-Notebook").wait_for(state="visible", timeout=MAX_NOTEBOOK_READY_MS)
    notebook_ready_ms = round((time.perf_counter() - start) * 1000, 1)
    result = {
        "profile": profile,
        "notebook": notebook,
        "notebook_ready_ms": notebook_ready_ms,
        "requests": requests,
        "failed_requests": failures,
    }
    context.close()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=ROOT / "site/jupyterlite")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/jupyterlite-runtime.json")
    args = parser.parse_args()
    from playwright.sync_api import sync_playwright

    site_dir = args.site_dir if args.site_dir.is_absolute() else ROOT / args.site_dir
    server = serve(site_dir)
    base = "".join(
        ("http", "://", server.server_address[0], ":", str(server.server_address[1]), "/")
    )
    results = []
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for profile, config in PROFILE_CONFIGS.items():
            try:
                result = measure(browser, base, profile, config["notebooks"][0])
                results.append(result)
                if result["notebook_ready_ms"] > MAX_NOTEBOOK_READY_MS:
                    errors.append(f"{profile}: excede {MAX_NOTEBOOK_READY_MS} ms")
                if result["requests"] > MAX_REQUESTS:
                    errors.append(f"{profile}: excede {MAX_REQUESTS} solicitudes")
                if result["failed_requests"]:
                    errors.append(f"{profile}: solicitudes fallidas")
            except Exception as error:  # Playwright proporciona el diagnóstico completo.
                errors.append(f"{profile}: {error}")
        browser.close()
    server.shutdown()
    report = {
        "budgets": {
            "notebook_ready_ms": MAX_NOTEBOOK_READY_MS,
            "requests": MAX_REQUESTS,
        },
        "profiles": results,
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
