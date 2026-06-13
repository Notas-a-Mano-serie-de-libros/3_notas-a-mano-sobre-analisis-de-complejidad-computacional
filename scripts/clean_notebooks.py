from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def clean_notebook(path: Path, check=False) -> bool:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs") != []:
            cell["outputs"] = []
            changed = True
        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            changed = True

    if changed and not check:
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Elimina outputs y execution_count de notebooks.")
    parser.add_argument("--check", action="store_true", help="Solo verifica; falla si encuentra notebooks sucios.")
    args = parser.parse_args()

    changed_paths = [
        path
        for path in sorted(PROJECT_ROOT.rglob("*.ipynb"))
        if ".ipynb_checkpoints" not in path.parts and clean_notebook(path, check=args.check)
    ]

    for path in changed_paths:
        print(path.relative_to(PROJECT_ROOT))

    if args.check and changed_paths:
        sys.exit(1)


if __name__ == "__main__":
    main()
