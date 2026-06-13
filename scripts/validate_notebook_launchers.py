from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ("capitulo7", "capitulo8")


def assignment_value(source: str, name: str):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    return None


def notebook_code_sources(path: Path) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return [
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    ]


def bootstrap_launchers(chapter: str) -> dict[str, str]:
    bootstrap_source = (PROJECT_ROOT / chapter / "notebooks" / "colab_bootstrap.py").read_text(encoding="utf-8")
    value = assignment_value(bootstrap_source, "SIMULATION_LAUNCHERS")
    if not isinstance(value, dict):
        raise AssertionError(f"{chapter}/notebooks/colab_bootstrap.py no define SIMULATION_LAUNCHERS")
    return value


def validate_notebook(path: Path, launchers: dict[str, str]) -> list[str]:
    errors = []
    sources = notebook_code_sources(path)
    joined = "\n".join(sources)
    simulation_name = None
    for source in sources:
        value = assignment_value(source, "SIMULATION_NAME")
        if value is not None:
            simulation_name = value
            break

    if simulation_name is None:
        errors.append(f"{path.relative_to(PROJECT_ROOT)} no define SIMULATION_NAME")
        return errors

    if simulation_name not in launchers:
        errors.append(f"{path.relative_to(PROJECT_ROOT)} usa SIMULATION_NAME={simulation_name!r}, pero no existe launcher")
    if "colab_bootstrap.py" not in joined and "BOOTSTRAP_URL" not in joined:
        errors.append(f"{path.relative_to(PROJECT_ROOT)} no carga colab_bootstrap.py")
    if "exec(" not in joined:
        errors.append(f"{path.relative_to(PROJECT_ROOT)} no ejecuta el bootstrap")

    return errors


def main() -> None:
    errors = []
    for chapter in CHAPTERS:
        launchers = bootstrap_launchers(chapter)
        for notebook_path in sorted((PROJECT_ROOT / chapter / "notebooks").glob("*.ipynb")):
            errors.extend(validate_notebook(notebook_path, launchers))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)

    print("Launchers de notebooks validados.")


if __name__ == "__main__":
    main()
