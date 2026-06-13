from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSIENT_CELL_METADATA = {
    "ExecuteTime",
    "execution",
}


def notebook_issues(notebook: dict) -> list[str]:
    issues = []

    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        metadata = cell.get("metadata", {})
        for key in sorted(TRANSIENT_CELL_METADATA):
            if key in metadata:
                issues.append(f"celda {index}: metadata.{key}")
        if cell.get("outputs") != []:
            issues.append(f"celda {index}: outputs")
        if cell.get("execution_count") is not None:
            issues.append(f"celda {index}: execution_count")

    return issues


def clean_notebook_data(notebook: dict) -> bool:
    changed = bool(notebook_issues(notebook))

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        metadata = cell.get("metadata", {})
        for key in TRANSIENT_CELL_METADATA:
            metadata.pop(key, None)
        cell["outputs"] = []
        cell["execution_count"] = None

    return changed


def clean_notebook(path: Path, check=False) -> tuple[bool, list[str]]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    issues = notebook_issues(notebook)
    changed = bool(issues)

    if changed and not check:
        clean_notebook_data(notebook)
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    return changed, issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Elimina outputs y execution_count de notebooks.")
    parser.add_argument("--check", action="store_true", help="Solo verifica; falla si encuentra notebooks sucios.")
    parser.add_argument("--diagnose", action="store_true", help="Muestra la celda y el campo que ensucian cada notebook.")
    args = parser.parse_args()

    changed_paths = []
    for path in sorted(PROJECT_ROOT.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        changed, issues = clean_notebook(path, check=args.check)
        if changed:
            changed_paths.append((path, issues))

    for path, issues in changed_paths:
        print(path.relative_to(PROJECT_ROOT))
        if args.diagnose:
            for issue in issues:
                print(f"  - {issue}")

    if args.check and changed_paths:
        sys.exit(1)


if __name__ == "__main__":
    main()
