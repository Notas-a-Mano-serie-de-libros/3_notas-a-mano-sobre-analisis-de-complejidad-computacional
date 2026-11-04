from __future__ import annotations

import json
import re
from pathlib import Path

from desarrollo.scripts.jupyterlite_catalog import CHAPTER_CONFIGS, CHAPTER_PROFILES, profile_content_files

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = re.compile(r"/main/((?:core|common|simulaciones)/[\w/\-.]+\.py)")
PROJECT_PATH = re.compile(r"""["']((?:core|common)/[\w/\-.]+\.py)["']""")


def test_notebook_remote_fallbacks_are_bundled() -> None:
    missing: list[str] = []
    for chapter in CHAPTER_CONFIGS:
        bundled = {path.as_posix() for path in profile_content_files(CHAPTER_PROFILES[chapter])}
        for notebook in CHAPTER_CONFIGS[chapter]["notebooks"]:
            data = json.loads((PROJECT_ROOT / notebook).read_text(encoding="utf-8"))
            source = "\n".join("".join(cell["source"]) for cell in data["cells"])
            for path in set(RAW_PATH.findall(source)) | set(PROJECT_PATH.findall(source)):
                if path not in bundled and not path.endswith(("__init__.py",)):
                    missing.append(f"{notebook.as_posix()} -> {path}")
    assert not missing, "\n".join(sorted(missing))
