"""Valida enlaces locales, rutas remotas del repositorio y ubicaciones obsoletas."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_NAME = "3_notas-a-mano-sobre-analisis-de-complejidad-computacional"
TEXT_SUFFIXES = {".md", ".ipynb", ".py"}
IGNORED_PARTS = {".git", ".pytest_cache", "__pycache__"}
OBSOLETE_PATTERNS = {
    r"capitulo[2-8]/graficas/": "carpeta antigua de gráficas del capítulo",
    r"(?:^|[\"'/])graficas/(?:recursos|generadas)/": "carpeta central de gráficas eliminada",
    r"capitulo[2-8]/images/capitulo[2-8]/": "capítulo duplicado dentro de images",
    r"capitulo[78]/notebooks/(?:colab_bootstrap|launchers)\.py": "lógica dentro de notebooks",
    r"capitulo[2-6]/colab_bootstrap\.py": "bootstrap fuera de runtime",
    r"capitulo4/referencias/util\.py": "utilidad antigua del capítulo 4",
}


def repository_files() -> list[Path]:
    return sorted(
        path
        for path in PROJECT_ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_SUFFIXES
        and not IGNORED_PARTS.intersection(path.parts)
    )


def notebook_markdown(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "markdown"
    )


def rendered_text(path: Path) -> str:
    if path.suffix == ".ipynb":
        return notebook_markdown(path)
    return path.read_text(encoding="utf-8")


def markdown_targets(text: str) -> list[str]:
    """Extrae destinos Markdown respetando paréntesis dentro del nombre."""

    targets: list[str] = []
    cursor = 0
    while True:
        marker = text.find("](", cursor)
        if marker < 0:
            break
        index = marker + 2
        depth = 1
        start = index
        while index < len(text) and depth:
            if text[index] == "(":
                depth += 1
            elif text[index] == ")":
                depth -= 1
            index += 1
        if depth == 0:
            target = text[start : index - 1].strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            targets.append(target)
        cursor = max(index, marker + 2)
    return targets


def link_targets(text: str) -> list[str]:
    html_targets = re.findall(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", text)
    return markdown_targets(text) + html_targets


def raw_urls(text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s\"'<>]+", text)
    cleaned: list[str] = []
    for url in urls:
        # En el JSON de un notebook el salto de línea posterior a un enlace se
        # representa literalmente como ``\\n``.
        url = url.removesuffix("\\n")
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
        cleaned.append(url.rstrip("\\}.,;"))
    return cleaned


def quoted_repository_paths(text: str) -> list[str]:
    """Extrae rutas literales de código que parten de un área del repositorio."""

    return re.findall(
        r"[\"']((?:capitulo[2-8]|common|core|scripts)/[^\"']+)[\"']",
        text,
    )


def clean_target(target: str) -> str:
    target = target.strip()
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return target.split("#", 1)[0].split("?", 1)[0]


def local_target_error(source: Path, target: str) -> str | None:
    cleaned = clean_target(target)
    if not cleaned or cleaned.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    destination = (source.parent / unquote(cleaned)).resolve()
    if not destination.exists():
        return f"{source.relative_to(PROJECT_ROOT)} enlaza un destino inexistente: {target}"
    return None


def repository_url_path(url: str) -> str | None:
    parsed = urlparse(url)
    if REPOSITORY_NAME not in parsed.path:
        return None
    components = [component for component in parsed.path.split("/") if component]
    try:
        repository_index = components.index(REPOSITORY_NAME)
        main_index = components.index("main", repository_index + 1)
    except ValueError:
        return None
    return unquote("/".join(components[main_index + 1 :]))


def remote_target_error(source: Path, target: str) -> str | None:
    if not target.startswith(("http://", "https://")):
        return None
    relative_path = repository_url_path(target)
    if relative_path is None:
        return None
    destination = PROJECT_ROOT / relative_path
    if not destination.exists():
        return (
            f"{source.relative_to(PROJECT_ROOT)} apunta a una ruta remota inexistente: "
            f"{relative_path}"
        )
    return None


def quoted_path_error(source: Path, target: str) -> str | None:
    target = target.rstrip("\\")
    if "\\" in target:
        return None
    if any(character in target for character in "*{}[]"):
        return None
    destination = PROJECT_ROOT / target
    if not destination.exists():
        return f"{source.relative_to(PROJECT_ROOT)} referencia una ruta inexistente: {target}"
    return None


def validate_repository_paths() -> list[str]:
    errors: list[str] = []
    for source in repository_files():
        raw_text = source.read_text(encoding="utf-8")
        for pattern, description in OBSOLETE_PATTERNS.items():
            if re.search(pattern, raw_text, flags=re.MULTILINE):
                errors.append(
                    f"{source.relative_to(PROJECT_ROOT)} conserva {description}: {pattern}"
                )

        targets = raw_urls(raw_text)
        if source.suffix in {".md", ".ipynb"}:
            targets.extend(link_targets(rendered_text(source)))
        for target in targets:
            for validator in (local_target_error, remote_target_error):
                error = validator(source, target)
                if error:
                    errors.append(error)
        for target in quoted_repository_paths(raw_text):
            error = quoted_path_error(source, target)
            if error:
                errors.append(error)
    return sorted(set(errors))


def main() -> int:
    errors = validate_repository_paths()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Rutas y enlaces del repositorio validados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
