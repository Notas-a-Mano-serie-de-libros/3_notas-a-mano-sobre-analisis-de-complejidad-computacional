from __future__ import annotations

import shutil
import stat
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOOKS_SOURCE = PROJECT_ROOT / "scripts" / "git_hooks"
HOOKS_TARGET = PROJECT_ROOT / ".git" / "hooks"


def install_hook(name: str) -> Path:
    source = HOOKS_SOURCE / name
    target = HOOKS_TARGET / name
    if not source.exists():
        raise FileNotFoundError(source)
    HOOKS_TARGET.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return target


def main() -> None:
    installed = install_hook("pre-commit")
    print(f"Hook instalado: {installed.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
