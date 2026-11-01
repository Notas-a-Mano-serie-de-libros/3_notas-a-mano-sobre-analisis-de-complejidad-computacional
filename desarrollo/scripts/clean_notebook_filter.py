from __future__ import annotations

import json
import sys

from clean_notebooks import clean_notebook_data


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        notebook = json.loads(raw)
    except json.JSONDecodeError:
        sys.stdout.write(raw)
        return
    clean_notebook_data(notebook)
    sys.stdout.write(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
