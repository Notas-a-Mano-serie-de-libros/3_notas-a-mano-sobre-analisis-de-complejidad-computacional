"""Compila los mismos programas Java mostrados en Pages (Java 8)."""

import json
from pathlib import Path
import subprocess
import tempfile
from java_examples import java_example

ROOT = Path(__file__).resolve().parents[1]


def build():
    catalog = json.loads((ROOT / "scripts/data/book_code.json").read_text())
    programs = {}
    metadata = {}
    for listings in catalog["pages"].values():
        for listing in listings:
            source, inputs, name = java_example(listing)
            programs[name] = source
            metadata[name] = listing
    with tempfile.TemporaryDirectory(prefix="pages-java-") as folder:
        work = Path(folder)
        for name, source in programs.items():
            (work / f"{name}.java").write_text(source)
        sources = [*work.glob("*.java"), *(ROOT / "scripts/java/ejemplos").glob("*.java")]
        classes = work / "classes"
        classes.mkdir()
        result = subprocess.run(
            ["javac", "--release", "8", "-encoding", "UTF-8", "-d", str(classes), *[str(p) for p in sources]], capture_output=True, text=True
        )
        if result.returncode:
            raise RuntimeError(result.stderr)
        target = ROOT / "docs/assets/java/ejemplos.jar"
        target.parent.mkdir(parents=True, exist_ok=True)

        def execute(name, encoded=""):
            run = subprocess.run(["java", "-cp", str(classes), "ejemplos.Runner", name, encoded], capture_output=True, text=True, timeout=30)
            if run.returncode:
                raise RuntimeError(name + run.stderr)
            return run.stdout

        for name, listing in metadata.items():
            output = execute(name)
            if listing["folio"] in (161, 166, 164):
                assert output.startswith("ERROR\n"), (name, output)
                continue
            assert output.startswith("OK\n"), (name, output)
            source, entries, _ = java_example(listing)
            if "public boolean buscar(int[]" in source:
                assert "Resultado: true" in output, (name, output)
                values = [literal for _, literal, _, _ in entries]
                values[-1] = "999"
                assert "Resultado: false" in execute(name, "\n".join(values)), name
                values[0] = "{}"
                for index, (_, _, _, variable) in enumerate(entries):
                    if variable == "b":
                        values[index] = "-1"
                assert "Resultado: false" in execute(name, "\n".join(values)), name
            elif "void ordenar(" in source:
                values = [literal for _, literal, _, _ in entries]
                values[0] = "{3, -1, 3}"
                assert "Arreglo ordenado: [-1, 3, 3]" in execute(name, "\n".join(values)), name
            elif listing["folio"] == 177:
                assert "Resultado: [[4, 4], [10, 8]]" in output, output
            elif listing["folio"] == 254:
                assert "Resultado: true" in output, output
                assert "Resultado: false" in execute(name, "5\n3\n9"), name
            elif listing["folio"] == 150:
                assert "Resultado: 5" in output, output
                assert "Resultado: -2147483648" in execute(name, "-2147483648\n0"), name
                assert execute(name, "2147483648\n0").startswith("ERROR\nNumberFormatException"), name
        subprocess.run(["jar", "cf", str(target), "-C", str(classes), "."], check=True)
        print(f"{len(programs)} programas Java compilados y sus main comprobados.")


if __name__ == "__main__":
    build()
