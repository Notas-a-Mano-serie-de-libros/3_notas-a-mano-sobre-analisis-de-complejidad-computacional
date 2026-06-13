from __future__ import annotations

import importlib.util
import math
import sys
import types
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class DummyScreen:
    def __init__(self, height: int = 600):
        self._height = height

    def get_height(self) -> int:
        return self._height


def load_module_from_path(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar el módulo {module_name} desde {path}")

    module = importlib.util.module_from_spec(spec)
    previous_module = sys.modules.get(module_name)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if previous_module is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous_module
    return module


def load_algorithm_module(script_path: Path, util_module_name: str, util_path: Path):
    util_module = load_module_from_path(util_module_name, util_path)
    script_source = script_path.read_text(encoding="utf-8")
    prefix = script_source.split("os.environ['SDL_VIDEO_CENTERED'] = '1'", 1)[0]

    module = types.ModuleType(script_path.stem)
    module.__file__ = str(script_path)

    previous_animation_utils = sys.modules.get("animation_utils")
    sys.modules["animation_utils"] = util_module
    try:
        exec(compile(prefix, str(script_path), "exec"), module.__dict__)
    finally:
        if previous_animation_utils is None:
            sys.modules.pop("animation_utils", None)
        else:
            sys.modules["animation_utils"] = previous_animation_utils

    return module, util_module


def make_search_nodes(util_module, values):
    default_fill, default_border, default_text = util_module.color_sets["default"]
    return [
        util_module.Nodo(
            width=util_module.BOX_WIDTH,
            height=util_module.BOX_HEIGHT,
            x=index * (util_module.BOX_WIDTH + util_module.SPACING),
            y=0,
            elemento=value,
            indice=index,
            fill_color=default_fill,
            border_color=default_border,
            text_color=default_text,
        )
        for index, value in enumerate(values)
    ]


def make_bar_nodes(util_module, values):
    default_fill, default_border, default_text = util_module.color_sets["default"]
    return [
        util_module.Nodo(
            width=40,
            height=value + 1,
            x=index * 50,
            y=0,
            elemento=value,
            indice=index,
            fill_color=default_fill,
            border_color=default_border,
            text_color=default_text,
        )
        for index, value in enumerate(values)
    ]


def run_search_algorithm(module, state, max_steps: int = 200):
    steps = 0
    while not state["search_complete"]:
        module.buscar(state)
        steps += 1
        if steps > max_steps:
            raise AssertionError(f"{module.__file__} excedió el máximo de pasos")
    return steps


def run_sort_algorithm(module, state, max_steps: int = 500):
    steps = 0
    while not state["sorting_complete"]:
        module.ordenar(state)
        steps += 1
        if steps > max_steps:
            raise AssertionError(f"{module.__file__} excedió el máximo de pasos")
    return steps


def build_jump_size(values) -> int:
    return int(math.sqrt(len(values)))
