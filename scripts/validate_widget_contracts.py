"""Valida dimensiones y ayudas accesibles de controles compartidos."""

from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.widget_controls import magnitude_stepper


CONTRACT_PATH = PROJECT_ROOT / "tests" / "fixtures" / "widget_contracts.json"


def current_contract():
    control = magnitude_stepper(value=30, accessible_name="Puntos de muestreo")
    return {
        "magnitude_stepper": {
            "container_width": control.container.layout.width,
            "field_width": control.value.layout.width,
            "button_width": control.previous.layout.width,
            "placeholder": control.value.placeholder,
            "previous_tooltip": control.previous.tooltip,
            "following_tooltip": control.following.tooltip,
        }
    }


def main():
    expected = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    actual = current_contract()
    if actual != expected:
        raise SystemExit(
            "El contrato visual de widgets cambió. Actualiza la implementación "
            "o tests/fixtures/widget_contracts.json de forma intencional."
        )
    print("Contratos visuales y accesibles de widgets validados.")


if __name__ == "__main__":
    main()
