"""Rutas homogéneas para las imágenes generadas de cada capítulo."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _chapter_graphics_root(parts: tuple[str, ...]) -> tuple[Path, tuple[str, ...]]:
    if not parts or not parts[0].startswith("capitulo"):
        raise ValueError("La ruta debe comenzar con el capítulo, por ejemplo 'capitulo2'.")
    chapter, *remaining = parts
    return PROJECT_ROOT / chapter / "images" / "generadas", tuple(remaining)


def graphics_dir(*parts: str) -> Path:
    """Devuelve y crea una subcarpeta de imágenes generadas del capítulo."""

    root, remaining = _chapter_graphics_root(parts)
    destination = root.joinpath(*remaining)
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def graphics_path(*parts: str) -> Path:
    """Construye una ruta de salida y crea su directorio contenedor."""

    root, remaining = _chapter_graphics_root(parts)
    destination = root.joinpath(*remaining)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination
