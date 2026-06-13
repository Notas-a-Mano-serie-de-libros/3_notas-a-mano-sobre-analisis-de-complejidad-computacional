from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = PROJECT_ROOT / "tests" / "fixtures" / "html_snapshots.json"
CAP7_DOMAIN = PROJECT_ROOT / "capitulo7" / "domain"
CAP8_DOMAIN = PROJECT_ROOT / "capitulo8" / "domain"


def load_module(name: str, path: Path, extra_paths=()):
    for extra_path in (PROJECT_ROOT, *extra_paths):
        value = str(extra_path)
        if value not in sys.path:
            sys.path.insert(0, value)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest_html(html: str) -> dict[str, int | str]:
    encoded = html.encode("utf-8")
    return {
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "bytes": len(encoded),
    }


def build_snapshots() -> dict[str, dict[str, int | str]]:
    snapshots = {}
    search_values = [2, 4, 6, 8, 10, 12, 14, 16]
    for name, filename in (
        ("secuencial", "1_busqueda_secuencial_app.py"),
        ("binaria", "2_busqueda_binaria_app.py"),
        ("interpolacion", "3_busqueda_interpolacion_app.py"),
        ("saltos", "4_busqueda_saltos_app.py"),
        ("exponencial", "5_busqueda_exponencial_app.py"),
        ("ternaria", "6_busqueda_ternaria_app.py"),
    ):
        module = load_module(f"snapshot_cap7_{name}", CAP7_DOMAIN / filename, extra_paths=(CAP7_DOMAIN,))
        state = module.create_state(size=len(search_values), target=10, values=search_values)
        snapshots[f"capitulo7.{name}.initial"] = digest_html(module.render_state_html(state))

    comparison = load_module("snapshot_cap7_comparacion", CAP7_DOMAIN / "0_comparacion_busquedas_app.py", extra_paths=(CAP7_DOMAIN,))
    state = comparison.create_comparison_state(size=len(search_values), target=10, values=search_values)
    snapshots["capitulo7.comparacion.initial"] = digest_html(comparison.render_comparison_html(state))

    sort_values = [9, 3, 7, 1, 8, 2, 6, 4]
    for name, filename, view in (
        ("burbuja", "1_ordenamiento_burbuja_app.py", "barras"),
        ("seleccion", "2_ordenamiento_seleccion_app.py", "barras"),
        ("insercion", "3_ordenamiento_insercion_app.py", "barras"),
        ("shell", "4_ordenamiento_shell_app.py", "barras"),
        ("mezcla", "5_ordenamiento_mezcla_app.py", "arbol"),
        ("rapido", "6_ordenamiento_rapido_app.py", "arbol"),
        ("radix", "7_ordenamiento_radix_app.py", "barras"),
    ):
        module = load_module(f"snapshot_cap8_{name}", CAP8_DOMAIN / filename, extra_paths=(CAP8_DOMAIN,))
        state = module.create_state(size=len(sort_values), values=sort_values, view=view)
        snapshots[f"capitulo8.{name}.{view}.initial"] = digest_html(module.render_state_html(state))

    comparison = load_module("snapshot_cap8_comparacion", CAP8_DOMAIN / "0_comparacion_ordenamientos_app.py", extra_paths=(CAP8_DOMAIN,))
    state = comparison.create_comparison_state(size=len(sort_values), values=sort_values)
    snapshots["capitulo8.comparacion.initial"] = digest_html(comparison.render_comparison_html(state))
    return snapshots


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida snapshots estructurales del HTML de las animaciones.")
    parser.add_argument("--update", action="store_true", help="Actualiza el archivo de snapshots.")
    args = parser.parse_args()

    current = build_snapshots()
    if args.update:
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_PATH.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Snapshots actualizados en {SNAPSHOT_PATH.relative_to(PROJECT_ROOT)}.")
        return

    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    if current != expected:
        print("Los snapshots HTML cambiaron. Ejecuta scripts/validate_html_snapshots.py --update si el cambio es intencional.", file=sys.stderr)
        expected_keys = set(expected)
        current_keys = set(current)
        for key in sorted(expected_keys ^ current_keys):
            print(f"- clave distinta: {key}", file=sys.stderr)
        for key in sorted(expected_keys & current_keys):
            if expected[key] != current[key]:
                print(f"- {key}: esperado {expected[key]}, actual {current[key]}", file=sys.stderr)
        sys.exit(1)

    print("Snapshots HTML validados.")


if __name__ == "__main__":
    main()
