"""Sincroniza las incrustaciones con los perfiles del catálogo JupyterLite."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from desarrollo.scripts.jupyterlite_catalog import (
        PAGE_NOTEBOOKS,
        profile_for_chapter,
    )
except ModuleNotFoundError:
    from jupyterlite_catalog import PAGE_NOTEBOOKS, profile_for_chapter


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
DEMO_START = "<!-- jupyterlite-demo:start -->"
DEMO_END = "<!-- jupyterlite-demo:end -->"


def notebook_url(chapter: int, notebook: Path) -> str:
    profile = profile_for_chapter(chapter)
    encoded_path = str(notebook).replace("/", "%2F")
    return f"jupyterlite/{profile}/notebooks/index.html?path={encoded_path}"


def normalize_demo_presentation(content: str) -> str:
    """Mantiene título y acciones encima de cada iframe JupyterLite."""

    def normalize(match: re.Match[str]) -> str:
        demo = match.group("demo")
        demo = re.sub(
            r'(<div class="jupyterlite-demo__toolbar">\s*<span>).*?(</span>)',
            r"\1Simulación interactiva\2",
            demo,
            count=1,
            flags=re.DOTALL,
        )
        demo = re.sub(
            r'(<a\b[^>]*class="[^"]*\bcolab-button\b[^"]*"[^>]*>).*?(</a>)',
            r"\1Abrir en Colab\2",
            demo,
            flags=re.DOTALL,
        )
        actions_match = re.search(
            r'(?P<actions>[ \t]*<div class="jupyterlite-demo__actions">.*?</div>)[ \t]*\n?',
            demo,
            flags=re.DOTALL,
        )
        if not actions_match:
            return match.group(0)

        action_lines = actions_match.group("actions").splitlines()
        base_indent = len(action_lines[0]) - len(action_lines[0].lstrip())
        actions = "\n".join(
            "  " + line[base_indent:] if line.strip() else ""
            for line in action_lines
        )
        demo_without_actions = (
            demo[: actions_match.start()] + demo[actions_match.end() :]
        )
        toolbar_match = re.search(
            r'<div class="jupyterlite-demo__toolbar">.*?</div>',
            demo_without_actions,
            flags=re.DOTALL,
        )
        if not toolbar_match:
            return match.group(0)

        insertion = toolbar_match.end()
        normalized = (
            demo_without_actions[:insertion].rstrip()
            + "\n"
            + actions
            + "\n"
            + demo_without_actions[insertion:].lstrip("\n")
        )
        return f"{DEMO_START}{normalized}{DEMO_END}"

    pattern = re.compile(
        rf"{re.escape(DEMO_START)}(?P<demo>.*?){re.escape(DEMO_END)}",
        flags=re.DOTALL,
    )
    return pattern.sub(normalize, content)


def synchronize(check: bool = False) -> list[Path]:
    changed = []
    errors = []
    for (chapter, page), notebooks in PAGE_NOTEBOOKS.items():
        path = (
            DOCS / "capitulos" / f"capitulo-{chapter}.md"
            if page == "__chapter__"
            else DOCS / "capitulos" / f"capitulo-{chapter}" / f"{page}.md"
        )
        if not path.is_file():
            errors.append(f"Falta la página catalogada: {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8")
        updated = normalize_demo_presentation(content)
        for notebook in notebooks:
            target = notebook_url(chapter, notebook)
            previous = f"jupyterlite/capitulo-{chapter}/notebooks/index.html?path={str(notebook).replace('/', '%2F')}"
            if previous in updated:
                updated = updated.replace(previous, target)
            elif target not in updated:
                errors.append(
                    f"{path.relative_to(ROOT)}: no se encontró la incrustación de {notebook}"
                )
        if updated != content:
            changed.append(path)
            if not check:
                path.write_text(updated, encoding="utf-8")
    if errors:
        raise ValueError("\n".join(errors))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = synchronize(check=args.check)
    if args.check and changed:
        for path in changed:
            print(f"URL JupyterLite desactualizada: {path.relative_to(ROOT)}")
        return 1
    print("URLs JupyterLite sincronizadas con el catálogo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
