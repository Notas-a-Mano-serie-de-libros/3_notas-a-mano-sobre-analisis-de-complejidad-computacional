from __future__ import annotations

import json
import re
from urllib.parse import urlparse

from tests.helpers import PROJECT_ROOT


PAGES_HOST = "notas-a-mano-serie-de-libros.github.io"
BUTTON_CLASS = 'class="notebook-pages-button"'
PAGES_BUTTON_IMAGE = "img.shields.io/badge/"


def test_every_notebook_pages_link_uses_the_styled_button():
    linked_notebooks = []

    for path in sorted(PROJECT_ROOT.glob("capitulo*/notebooks/**/*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook.get("cells", []):
            source = "".join(cell.get("source", []))
            if PAGES_HOST not in source:
                continue

            linked_notebooks.append(path)
            assert cell.get("cell_type") == "markdown", path
            assert BUTTON_CLASS in source, path
            assert PAGES_BUTTON_IMAGE in source, path
            assert "logo=github" in source, path
            assert "cdn.simpleicons.org/githubpages/" not in source, path
            assert "cdn.simpleicons.org/github/" not in source, path
            assert "raw.githubusercontent.com" not in source, path
            assert 'alt="Leer la explicación completa en GitHub Pages"' in source, path
            assert 'target="_blank"' in source, path
            assert 'rel="noopener noreferrer"' in source, path
            assert "Leer la explicación completa en GitHub Pages" in source, path
            hrefs = re.findall(r'class="notebook-pages-button" href="([^"]+)"', source)
            assert len(hrefs) == 1, path
            assert hrefs[0].startswith(f"https://{PAGES_HOST}/"), path
            assert hrefs[0].endswith("/"), path
            assert "](" not in hrefs[0], path
            assert "/laboratorios/" not in hrefs[0], path

            published_path = urlparse(hrefs[0]).path.split(
                "/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/",
                1,
            )[1].rstrip("/")
            source_page = (PROJECT_ROOT / "docs" / published_path).with_suffix(".md")
            assert source_page.is_file(), (path, source_page)

    assert linked_notebooks
    assert len(linked_notebooks) == len(set(linked_notebooks))
