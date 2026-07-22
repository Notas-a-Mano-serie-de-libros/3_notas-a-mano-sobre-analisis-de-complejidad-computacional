"""Carga las simulaciones interactivas de notación asintótica del capítulo 3."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import urllib.request


RAW_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo3/asymptotic_animation.py"

APP_FUNCTIONS = {
    "big_o": "run_big_o_app",
    "little_o": "run_little_o_app",
    "big_omega": "run_big_omega_app",
    "little_omega": "run_little_omega_app",
    "theta": "run_theta_app",
}


def find_animation_module():
    candidates = (
        Path("../asymptotic_animation.py"),
        Path("capitulo3/asymptotic_animation.py"),
        Path("asymptotic_animation.py"),
    )
    module_path = next((candidate for candidate in candidates if candidate.exists()), None)
    if module_path is not None:
        return module_path

    module_path = Path("asymptotic_animation.py")
    request = urllib.request.Request(RAW_URL, headers={"Cache-Control": "no-cache"})
    module_path.write_bytes(urllib.request.urlopen(request).read())
    return module_path


def load_animation_module(module_path):
    spec = importlib.util.spec_from_file_location("cap3_asymptotic_animation", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


app_name = globals().get("ASYMPTOTIC_APP", "big_o")
function_name = APP_FUNCTIONS[app_name]
animation_module = load_animation_module(find_animation_module())
getattr(animation_module, function_name)()
