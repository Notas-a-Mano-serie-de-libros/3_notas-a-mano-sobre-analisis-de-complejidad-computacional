"""Compila y comprueba los ejemplos C con WASI SDK."""

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

try:
    from desarrollo.scripts.c_examples import c_example
except ModuleNotFoundError:
    from c_examples import c_example

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "docs/assets/c"


def source_hash(source, visible, folio):
    dependencies = [ROOT / "desarrollo/scripts/c/pages_inputs.h"]
    if folio == 167:
        dependencies += [ROOT / "desarrollo/scripts/c/vendor/mini-gmp.c", ROOT / "desarrollo/scripts/c/vendor/mini-gmp.h"]
    digest = hashlib.sha256((source + visible).encode())
    for path in dependencies:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def build(check=False):
    catalog = json.loads((ROOT / "desarrollo/scripts/data/book_code.json").read_text())
    programs = {}
    for items in catalog["pages"].values():
        for item in items:
            source, entries, key = c_example(item, runtime=True)
            visible, _, _ = c_example(item)
            programs[key] = (source, visible, item, entries)
    if check:
        manifest = json.loads((TARGET / "manifest.json").read_text())
        assert set(programs) == set(manifest)
        for key, (source, visible, item, _) in programs.items():
            assert manifest[key]["source"] == source_hash(source, visible, item["folio"]), f"Ejemplo C desactualizado: {key}"
            assert manifest[key]["wasm"] == hashlib.sha256((TARGET / f"{key}.wasm").read_bytes()).hexdigest(), f"WebAssembly C inválido: {key}"
        print(f"{len(programs)} módulos C vigentes.")
        return
    sdk = os.environ.get("WASI_SDK_PATH")
    if not sdk:
        raise RuntimeError("Define WASI_SDK_PATH con la ruta de WASI SDK 34, o usa --check para validar los módulos existentes.")
    clang = Path(sdk) / "bin/clang"
    TARGET.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with tempfile.TemporaryDirectory(prefix="pages-c-") as folder:
        for key, (source, visible, item, entries) in programs.items():
            src = Path(folder) / f"{key}.c"
            src.write_text(source)
            command = [str(clang), "-std=c11", "-O1", "-fwrapv", "-I" + str(ROOT / "desarrollo/scripts/c"), "-I" + str(ROOT / "desarrollo/scripts/c/vendor"), str(src)]
            if item["folio"] == 167:
                command.append(str(ROOT / "desarrollo/scripts/c/vendor/mini-gmp.c"))
            command += ["-lm", "-Wl,-z,stack-size=1048576", "-Wl,--max-memory=67108864", "-Wl,--strip-all", "-o", str(TARGET / f"{key}.wasm")]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f"Folio {item['folio']}: {result.stderr}")
            manifest[key] = {
                "source": source_hash(source, visible, item["folio"]),
                "wasm": hashlib.sha256((TARGET / f"{key}.wasm").read_bytes()).hexdigest(),
                "folio": item["folio"],
                "inputs": [name for _, _, _, name in entries],
                "args": [literal for _, literal, _, _ in entries],
            }
    for old in TARGET.glob("*.wasm"):
        if old.stem not in programs:
            old.unlink()
    (TARGET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"{len(programs)} programas C compilados a WebAssembly.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    build(parser.parse_args().check)
