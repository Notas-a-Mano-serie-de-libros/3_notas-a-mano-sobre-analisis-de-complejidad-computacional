from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = PROJECT_ROOT / "benchmarks" / "animation_baseline.json"


def benchmark_regressions(report: dict, baseline: dict) -> list[str]:
    budgets = baseline["max_avg_ms"]
    errors = []
    seen = set()
    for item in report["benchmarks"]:
        label = item["label"]
        seen.add(label)
        if label not in budgets:
            errors.append(f"{label}: no existe en la línea base")
            continue
        avg_ms = float(item["avg_ms"])
        max_ms = float(budgets[label])
        if avg_ms > max_ms:
            errors.append(f"{label}: avg={avg_ms:.3f} ms supera presupuesto {max_ms:.3f} ms")

    missing = sorted(set(budgets) - seen)
    for label in missing:
        errors.append(f"{label}: existe en línea base, pero no aparece en el reporte")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida un reporte de benchmark contra la línea base versionada.")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, default=BASELINE_PATH)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    errors = benchmark_regressions(report, baseline)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)
    print("Reporte de benchmark validado contra la línea base.")


if __name__ == "__main__":
    main()
