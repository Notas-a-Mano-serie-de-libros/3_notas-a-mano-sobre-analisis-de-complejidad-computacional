from __future__ import annotations

import shutil
import stat
import subprocess
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


def install_notebook_filter() -> None:
    clean_command = "python3 scripts/clean_notebook_filter.py"
    subprocess.run(["git", "config", "--local", "filter.strip-notebook-output.clean", clean_command], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "config", "--local", "filter.strip-notebook-output.smudge", "cat"], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "config", "--local", "filter.strip-notebook-output.required", "false"], cwd=PROJECT_ROOT, check=True)


def main() -> None:
    installed = install_hook("pre-commit")
    install_notebook_filter()
    print(f"Hook instalado: {installed.relative_to(PROJECT_ROOT)}")
    print("Filtro de notebooks instalado: strip-notebook-output")


if __name__ == "__main__":
    main()
