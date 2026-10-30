import json
from pathlib import Path

from PIL import Image

from desarrollo.scripts import sync_page_assets
from desarrollo.scripts.validate_page_assets import validate

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_pages_no_publica_imagenes_huerfanas():
    assert validate() == []


def test_recurrence_multiplicity_trees_have_a_transparent_canvas_and_opaque_nodes():
    image_dir = PROJECT_ROOT / "docs/assets/images/capitulo-5"
    for suffix in ("a1", "a2", "ak"):
        image = Image.open(image_dir / f"arbol_recurrencia_{suffix}.png").convert("RGBA")
        width, height = image.size
        assert all(
            image.getpixel(point)[3] == 0
            for point in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))
        )
        colors = {color: count for count, color in image.getcolors(maxcolors=width * height)}
        assert colors[(255, 255, 255, 255)] > 1_000


def test_image_sync_check_ignores_png_compression_but_detects_pixel_drift(
    tmp_path, monkeypatch
):
    source = tmp_path / "source.png"
    destination = tmp_path / "docs" / "assets" / "published.png"
    destination.parent.mkdir(parents=True)
    image = Image.new("RGBA", (4, 3), (20, 40, 60, 255))
    image.save(source, optimize=False)
    image.save(destination, optimize=True, compress_level=1)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps({"docs/assets/published.png": "source.png"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(sync_page_assets, "ROOT", tmp_path)
    monkeypatch.setattr(sync_page_assets, "MANIFEST", manifest)

    assert sync_page_assets.sync(check=True) == []

    image.putpixel((1, 1), (80, 90, 100, 255))
    image.save(destination, optimize=True, compress_level=1)
    assert sync_page_assets.sync(check=True) == [
        "Recurso desactualizado: docs/assets/published.png"
    ]
