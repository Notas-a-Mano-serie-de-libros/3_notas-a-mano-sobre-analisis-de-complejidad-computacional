"""Hook de MkDocs: cache-busting automático para assets locales.

Calcula un hash md5 corto del contenido de cada archivo CSS/JS local
declarado en ``extra_css``/``extra_javascript`` y lo añade como query
string (``?v=<hash8>``), evitando tener que versionar manualmente esas
rutas en ``mkdocs.yml`` cada vez que se editan. Las URLs externas
(que empiezan por ``http``) no se tocan.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from urllib.parse import urlsplit


def _hashed_path(path: str, docs_dir: Path) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path

    # Quita cualquier query string existente para ubicar el archivo real.
    relative_path = urlsplit(path).path
    file_path = docs_dir / relative_path

    if not file_path.is_file():
        # No se pudo resolver el archivo: se deja la ruta tal cual.
        return path

    digest = hashlib.md5(file_path.read_bytes()).hexdigest()[:8]
    return f"{relative_path}?v={digest}"


def on_config(config, **kwargs):
    docs_dir = Path(config["docs_dir"])

    # extra_css: lista de rutas planas (str).
    config["extra_css"] = [
        _hashed_path(entry, docs_dir) for entry in config.get("extra_css", [])
    ]

    # extra_javascript: cada entrada puede ser un str plano o un objeto
    # ExtraScriptValue (por ejemplo, los .mjs con type="module"). En este
    # último caso se conserva el objeto y solo se reescribe su .path.
    new_extra_javascript = []
    for script in config.get("extra_javascript", []):
        if isinstance(script, str):
            new_extra_javascript.append(_hashed_path(script, docs_dir))
        else:
            script.path = _hashed_path(str(script), docs_dir)
            new_extra_javascript.append(script)
    config["extra_javascript"] = new_extra_javascript

    return config
