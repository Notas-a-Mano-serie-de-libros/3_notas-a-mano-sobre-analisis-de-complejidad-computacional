"""Descargas pequeñas y acotadas usadas por los cargadores de Colab."""

from __future__ import annotations

import time
import urllib.request


def read_text(url: str, *, timeout: float = 30, retries: int = 2) -> str:
    """Lee un recurso remoto con timeout y reintentos limitados."""
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
            )
            try:
                response = urllib.request.urlopen(request, timeout=timeout)
            except TypeError:
                # Permite adaptadores simples usados por los validadores y tests.
                response = urllib.request.urlopen(request)
            if hasattr(response, "__enter__"):
                with response:
                    return response.read().decode("utf-8")
            return response.read().decode("utf-8")
        except (OSError, TimeoutError) as error:
            last_error = error
            if attempt < retries:
                time.sleep(0.5 * (2 ** attempt))
    raise RuntimeError(f"No se pudo descargar el recurso remoto: {url}") from last_error
