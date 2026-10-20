from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = ("capitulo7", "capitulo8")
RUNTIME_REVISION = (
    PROJECT_ROOT / "desarrollo/scripts/data/runtime_revision.txt"
).read_text(encoding="utf-8").strip()
RAW_URL = re.compile(
    r"https://raw\.githubusercontent\.com/Notas-a-Mano-serie-de-libros/"
    r"3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
    r"([^/\s\"'\\]+)(?:/|\"|'|\\n)"
)


def load_constant(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{path.relative_to(PROJECT_ROOT)} no define {name}")


def notebook_simulation_name(path: Path) -> str | None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook.get("cells", []):
        source = "".join(cell.get("source", []))
        if "SIMULATION_NAME" not in source:
            continue
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "SIMULATION_NAME":
                        return ast.literal_eval(node.value)
    return None


def validate_chapter(chapter: str) -> list[str]:
    errors = []
    bootstrap = PROJECT_ROOT / "simulaciones" / chapter / "runtime" / "colab_bootstrap.py"
    required_files = load_constant(bootstrap, "REQUIRED_FILES")
    launchers = load_constant(bootstrap, "SIMULATION_LAUNCHERS")
    bootstrap_source = bootstrap.read_text(encoding="utf-8")

    for relative_path in required_files:
        if not (PROJECT_ROOT / relative_path).exists():
            errors.append(f"{bootstrap.relative_to(PROJECT_ROOT)} referencia un archivo inexistente: {relative_path}")

    for simulation_name, launcher_name in launchers.items():
        if f"def {launcher_name}(" not in (PROJECT_ROOT / "simulaciones" / chapter / "runtime" / "launchers.py").read_text(encoding="utf-8"):
            errors.append(f"{chapter}: {simulation_name} apunta a un launcher inexistente: {launcher_name}")

    for marker in ("RAW_BASE_URL", "REQUIRED_FILES", "SIMULATION_LAUNCHERS", "ensure_colab_files", "resolve_launcher_path"):
        if marker not in bootstrap_source:
            errors.append(f"{bootstrap.relative_to(PROJECT_ROOT)} no contiene {marker}")

    for notebook_path in sorted((PROJECT_ROOT / "simulaciones" / chapter / "notebooks").glob("[0-9]_*.ipynb")):
        simulation_name = notebook_simulation_name(notebook_path)
        if simulation_name is None:
            errors.append(f"{notebook_path.relative_to(PROJECT_ROOT)} no define SIMULATION_NAME")
        elif simulation_name not in launchers:
            errors.append(
                f"{notebook_path.relative_to(PROJECT_ROOT)} usa SIMULATION_NAME={simulation_name!r}, "
                f"pero el bootstrap no lo registra"
            )

    return errors


def main() -> None:
    errors = []
    for chapter in CHAPTERS:
        errors.extend(validate_chapter(chapter))

    for root_name in ("common", "core", "simulaciones", "desarrollo/scripts"):
        for path in (PROJECT_ROOT / root_name).rglob("*"):
            if not path.is_file() or path.suffix not in {".py", ".ipynb"}:
                continue
            if {".ipynb_checkpoints", ".virtual_documents"}.intersection(path.parts):
                continue
            for revision in RAW_URL.findall(path.read_text(encoding="utf-8")):
                if revision != RUNTIME_REVISION:
                    errors.append(
                        f"{path.relative_to(PROJECT_ROOT)} usa la revisión remota "
                        f"{revision}; se esperaba {RUNTIME_REVISION}"
                    )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)

    print("Bootstrap de Colab validado.")


if __name__ == "__main__":
    main()
