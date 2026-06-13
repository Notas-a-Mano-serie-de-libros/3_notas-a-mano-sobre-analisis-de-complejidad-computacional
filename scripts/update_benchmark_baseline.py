from __future__ import annotations

import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = PROJECT_ROOT / "benchmarks" / "animation_baseline.json"


def build_baseline(report: dict, multiplier: float, minimum_ms: float) -> dict:
    entries = {}
    for item in report["benchmarks"]:
        budget = max(float(item["avg_ms"]) * multiplier, minimum_ms)
        entries[item["label"]] = round(budget, 6)
    return {
        "description": "Presupuesto máximo por benchmark en milisegundos.",
        "max_avg_ms": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye la línea base de performance desde un reporte de benchmark.")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=BASELINE_PATH)
    parser.add_argument("--multiplier", type=float, default=8.0)
    parser.add_argument("--minimum-ms", type=float, default=5.0)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    baseline = build_baseline(report, args.multiplier, args.minimum_ms)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Línea base escrita en {args.output.relative_to(PROJECT_ROOT)}.")


if __name__ == "__main__":
    main()
