from __future__ import annotations

import json
import re
from pathlib import Path

from tests.helpers import PROJECT_ROOT


GRID_CALL = re.compile(r"\b(?:ax\w*|axis)\.grid\(([^)]*)\)")

SIMULATION_GRID_COUNTS = {
    "capitulo2/runtime/experimental_animation.py": 1,
    "capitulo2/runtime/polynomial_animation.py": 1,
    "capitulo4/runtime/experimental_analysis.py": 3,
    "capitulo7/runtime/exercise_laboratory.py": 2,
    "capitulo8/runtime/exercise_laboratory.py": 2,
    "common/chart_runtime.py": 1,
    "core/search/interpolation_visual.py": 2,
}


def _chart_sources():
    roots = [
        *sorted(PROJECT_ROOT.glob("capitulo[0-9]*")),
        PROJECT_ROOT / "common",
        PROJECT_ROOT / "core",
    ]
    for root in roots:
        for path in sorted(root.rglob("*.py")):
            yield path, path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*.ipynb")):
            notebook = json.loads(path.read_text(encoding="utf-8"))
            source = "\n".join(
                "".join(cell.get("source", []))
                for cell in notebook.get("cells", [])
                if cell.get("cell_type") == "code"
            )
            yield path, source


def test_all_matplotlib_grids_match_comparacion_big_o():
    calls = []
    for path, source in _chart_sources():
        calls.extend(
            (path.relative_to(PROJECT_ROOT), match.group(1).strip())
            for match in GRID_CALL.finditer(source)
        )

    assert calls
    assert all(arguments == "True" for _path, arguments in calls), calls


def test_all_cartesian_simulations_enable_the_reference_grid():
    for relative_path, expected_count in SIMULATION_GRID_COUNTS.items():
        source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        calls = [match.group(1).strip() for match in GRID_CALL.finditer(source)]

        assert calls == ["True"] * expected_count, relative_path

    shared_style = (
        PROJECT_ROOT / "capitulo2/runtime/experimental_animation.py"
    ).read_text(encoding="utf-8")
    assert "def style_experiment_axis(" in shared_style
    assert "ax.grid(True)" in shared_style

    for relative_path in (
        "capitulo2/runtime/constant_animation.py",
        "capitulo2/runtime/complexity_animations.py",
    ):
        source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        assert "style_experiment_axis(" in source, relative_path
