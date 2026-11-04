"""Serializa de forma determinista los recursos gráficos publicados."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path


def published_bytes(source: Path) -> bytes:
    if source.suffix.lower() != ".png":
        return source.read_bytes()

    from PIL import Image, ImageOps

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        output = BytesIO()
        image.save(output, format="PNG", optimize=True, compress_level=9)
        return output.getvalue()


def rendered_png_pixels(source: Path) -> tuple[tuple[int, int], bytes]:
    """Normalizes PNG pixels so sync checks ignore encoder-version differences."""

    from PIL import Image, ImageOps

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGBA")
        return image.size, image.tobytes()
