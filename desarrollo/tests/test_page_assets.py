from desarrollo.scripts.validate_page_assets import validate


def test_pages_no_publica_imagenes_huerfanas():
    assert validate() == []
