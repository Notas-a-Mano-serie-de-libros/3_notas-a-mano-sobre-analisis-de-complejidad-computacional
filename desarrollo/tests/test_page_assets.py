import json

from PIL import Image

from desarrollo.scripts import sync_page_assets
from desarrollo.scripts.validate_page_assets import validate


def test_pages_no_publica_imagenes_huerfanas():
    assert validate() == []


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
