"""Comprueba los cargadores de cada notebook en local y en un Colab aislado."""
from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import importlib.machinery
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]


def worker(notebook: Path, remote: bool, live: bool = False) -> list[str]:
    cells = json.loads(notebook.read_text())["cells"]
    import IPython.display
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    IPython.display.display = lambda *args, **kwargs: None
    IPython.display.clear_output = lambda *args, **kwargs: None
    plt.show = lambda *args, **kwargs: None
    Figure.savefig = lambda *args, **kwargs: None

    class Response(io.BytesIO):
        pass

    def source_path(url):
        if not remote:
            raise RuntimeError(f"El notebook local intentó descargar un recurso: {url}")
        url = url.full_url if hasattr(url, "full_url") else url
        path = unquote(urlparse(url).path).split("/main/", 1)
        if len(path) != 2:
            raise ValueError(f"Descarga externa no inventariada: {url}")
        return ROOT / path[1]

    original_urlopen = urllib.request.urlopen
    if live:
        import ssl

        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
        def live_urlopen(url, **kwargs):
            kwargs.setdefault("timeout", 30)
            kwargs.setdefault("context", context)
            return original_urlopen(url, **kwargs)
        urllib.request.urlopen = live_urlopen
    else:
        urllib.request.urlopen = lambda url, **kwargs: Response(source_path(url).read_bytes())

    def retrieve(url, filename=None, **kwargs):
        if filename:
            destination = Path(filename)
            with urllib.request.urlopen(url) as response:
                destination.write_bytes(response.read())
        else:
            with tempfile.NamedTemporaryFile(suffix=".download", delete=False) as temporary_file:
                destination = Path(temporary_file.name)
                with urllib.request.urlopen(url) as response:
                    temporary_file.write(response.read())
        return str(destination), None

    urllib.request.urlretrieve = retrieve
    if remote:
        google = types.ModuleType("google")
        google.__path__ = []
        colab = types.ModuleType("google.colab")
        colab.__spec__ = importlib.machinery.ModuleSpec("google.colab", loader=None, is_package=True)
        colab.__path__ = []
        output = types.ModuleType("google.colab.output")
        output.enable_custom_widget_manager = lambda: None
        colab.output = output
        google.colab = colab
        sys.modules.update({"google": google, "google.colab": colab, "google.colab.output": output})
        sys.path[:] = [path for path in sys.path if path and (".venv" in Path(path).parts or not str(Path(path).resolve()).startswith(str(ROOT)))]
    else:
        sys.path[:] = [path for path in sys.path if path and (".venv" in Path(path).parts or not str(Path(path).resolve()).startswith(str(ROOT)))]
    failures = []
    with tempfile.TemporaryDirectory() as temporary:
        tempfile.gettempdir = lambda: temporary
        os.chdir(temporary if remote else notebook.parent)
        namespace = {"__name__": "__main__"}
        for index, cell in enumerate(cells):
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell.get("source", []))
            # Comprueba la sintaxis de todas las celdas sin ejecutar mediciones
            # costosas. Se omiten magias y comandos de shell propios de Jupyter.
            compilable = "\n".join(
                line for line in source.splitlines()
                if not line.lstrip().startswith(("%", "!"))
            )
            try:
                compile(compilable, f"{notebook.name}:cell-{index + 1}", "exec")
            except (SyntaxError, ValueError) as error:
                failures.append(f"celda {index + 1}: {type(error).__name__}: {error}")
                continue
            # Ejecutar las celdas que cargan referencias, sin correr las mediciones largas.
            if not any(token in source for token in ("urlopen", "urlretrieve", "PROJECT_ROOT", "spec_from_file_location")):
                continue
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    exec(compile(source, f"{notebook.name}:cell-{index + 1}", "exec"), namespace)
            except Exception as error:
                failures.append(f"celda {index + 1}: {type(error).__name__}: {error}")
            plt.close("all")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path)
    parser.add_argument("--remote", action="store_true")
    parser.add_argument("--live", action="store_true", help="Carga el código publicado de GitHub en el modo remoto")
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker, args.remote, args.live)))
        return
    failures = []
    notebooks = sorted(path for path in (ROOT / "simulaciones").rglob("*.ipynb") if not {".ipynb_checkpoints", ".virtual_documents"}.intersection(path.parts))
    def audit(case):
        notebook, remote = case
        command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(notebook)]
        if remote:
            command.append("--remote")
            if args.live:
                command.append("--live")
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=180 if args.live else 40)
            issues = json.loads(result.stdout) if result.returncode == 0 else [result.stderr.strip()]
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as error:
            issues = [str(error)]
        return notebook, remote, issues

    cases = [(notebook, remote) for notebook in notebooks for remote in (False, True)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=1 if args.live else 4) as pool:
        for notebook, remote, issues in pool.map(audit, cases):
            mode = "Colab" if remote else "local"
            for issue in issues:
                failures.append(f"{notebook.relative_to(ROOT)} [{mode}] {issue}")
            print(f"{'ERROR' if issues else 'OK'} {mode}: {notebook.name}", flush=True)
    print("\n".join(failures))
    print(f"{len(notebooks)} notebooks; {len(notebooks) * 2} cargas; {len(failures)} fallos.")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
