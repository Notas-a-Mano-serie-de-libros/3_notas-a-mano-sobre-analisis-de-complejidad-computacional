"""Reproduce comprobaciones de compilación y comportamiento de los listados Java."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "scripts/data"


def run() -> None:
    inventory = json.loads((DATA / "book_review_listings.json").read_text())
    listings = inventory["listings"]
    binary = next(e["code"] for e in listings if e["folio"] == 268)
    prime = next(e["corrected_code"] for e in listings if "public boolean esPrimo(int" in e["code"])
    methods = [e for e in listings if e["code"].startswith("public ")]
    with tempfile.TemporaryDirectory(prefix="book-java-review-") as folder:
        work = Path(folder)
        for e in methods:
            code = e["corrected_code"]
            dependencies = ""
            if e["folio"] == 298 and "public boolean busquedaBinaria" not in code:
                dependencies += binary.replace("buscar(", "busquedaBinaria(")
            if "esPrimoAnidado" in code:
                dependencies += prime
            stubs = "\n".join(f"static void {name}(int... args) {{}}" for name in ("foo", "foo1", "foo2", "foo3"))
            wrapper = (
                "import java.util.*; import java.math.*;\n"
                f"class L{e['id']} {{\n"
                "static class Nodo { int dato; Nodo izquierdo, derecho; }\n" + stubs + "\n" + dependencies + "\n" + code + "\n}"
            )
            (work / f"L{e['id']}.java").write_text(wrapper)
        subprocess.run(["javac", *[str(p) for p in work.glob("*.java")]], check=True, capture_output=True, text=True)
        harness = ROOT / "scripts/book_review_checks.java"
        (work / "BookReviewChecks.java").write_text(harness.read_text())
        subprocess.run(["javac", "-cp", str(work), str(work / "BookReviewChecks.java")], check=True, capture_output=True, text=True)
        result = subprocess.run(["java", "-cp", str(work), "BookReviewChecks"], check=True, capture_output=True, text=True, timeout=60)
        evidence = json.loads(result.stdout)
    report = {
        "source_sha256": inventory["source_sha256"],
        "listings": len(listings),
        "method_listings_compiled": len(methods),
        "schematic_listings": len(listings) - len(methods),
        "compilation_context": "Java 17; imports java.util/java.math, clase Nodo y funciones foo vacías. Versiones corregidas; auxiliar binaria incluida en el listado exponencial.",
        "checks": evidence,
        "version": "corrected",
    }
    (DATA / "book_review_results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
