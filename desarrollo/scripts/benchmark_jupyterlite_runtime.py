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
# Estos límites protegen la experiencia, no solo evitan un timeout técnico.
# Se miden sobre archivos locales en Chromium; una regresión que tarde decenas
# de segundos debe fallar antes de llegar a producción.
MAX_NOTEBOOK_READY_MS = 15_000
# Incluye el arranque en frío de Pyodide e ipywidgets. Sigue siendo un límite
# estricto frente a la regresión de varios minutos causada por precargar el
# conjunto científico completo del perfil de búsquedas.
MAX_SIMULATION_READY_MS = 45_000
MAX_REQUESTS = 250
SIMULATION_CASES = (
    (
        "analisis-completo",
        Path("simulaciones/capitulo7/notebooks/1_busqueda_secuencial.ipynb"),
        ".search-simulation-root",
    ),
    (
        "graficas",
        Path("simulaciones/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb"),
        ".sort-simulation-root",
    ),
)


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


def verify_executed_simulation(
    browser, base: str, profile: str, notebook: Path, selector: str
) -> dict[str, object]:
    """Comprueba que el notebook se ejecuta y el navegador sigue respondiendo."""

    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    failures: list[str] = []
    unexpected_scientific_requests: list[str] = []
    page.on("requestfailed", lambda request: failures.append(request.url))

    def detect_unneeded_scientific_package(response) -> None:
        filename = response.url.rsplit("/", 1)[-1]
        if filename.startswith(("matplotlib-", "numpy-")):
            unexpected_scientific_requests.append(response.url)

    page.on("response", detect_unneeded_scientific_package)
    url = f"{base}{profile}/notebooks/index.html?path={quote(notebook.as_posix(), safe='')}"
    start = time.perf_counter()
    page.goto(url, wait_until="domcontentloaded", timeout=MAX_NOTEBOOK_READY_MS)
    simulation = page.locator(selector)
    simulation.wait_for(state="visible", timeout=MAX_SIMULATION_READY_MS)
    # Esta segunda consulta detecta regresiones que dibujan el widget y luego
    # bloquean el hilo principal mediante observadores DOM recursivos.
    responsive = simulation.is_visible()
    ready_ms = round((time.perf_counter() - start) * 1000, 1)
    context.close()
    return {
        "profile": profile,
        "notebook": notebook.as_posix(),
        "simulation_ready_ms": ready_ms,
        "responsive": responsive,
        "failed_requests": failures,
        "unexpected_scientific_requests": unexpected_scientific_requests,
    }


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
        # Los smokes deben ejecutarse antes de las aperturas superficiales de
        # perfiles. Esas aperturas cierran kernels mientras Pyodide descarga y
        # contaminarían la medición del arranque frío con solicitudes abortadas.
        simulation_smoke = []
        for profile, notebook, selector in SIMULATION_CASES:
            try:
                smoke = verify_executed_simulation(
                    browser, base, profile, notebook, selector
                )
                simulation_smoke.append(smoke)
                label = notebook.name
                if not smoke["responsive"]:
                    errors.append(f"{label}: el navegador dejó de responder")
                if smoke["failed_requests"]:
                    errors.append(f"{label}: solicitudes fallidas")
                if smoke["unexpected_scientific_requests"]:
                    errors.append(f"{label}: descargó dependencias científicas innecesarias")
            except Exception as error:
                errors.append(f"{notebook.name}: {error}")
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
            "simulation_ready_ms": MAX_SIMULATION_READY_MS,
            "requests": MAX_REQUESTS,
        },
        "profiles": results,
        "simulation_smoke": simulation_smoke,
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
