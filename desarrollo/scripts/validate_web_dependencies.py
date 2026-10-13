"""Valida versiones y fronteras de confianza de recursos web ejecutables."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEARCH_ROOTS = ("common", "core", "simulaciones", "docs")
TEXT_SUFFIXES = {".html", ".js", ".md", ".py"}
MATHJAX_BASE = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/"
MATHJAX_TEMPLATE_URL = "https://unpkg.com/mathjax@3.2.2/es5/tex-mml-chtml.js"
PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.mjs"
MATHJAX_SRI = "sha256-1CldwzdEg2k1wTmf7s5RWVd7NMXI/7nxxjJM2C4DqII="
CHEERPJ_URL = "https://cjrtnc.leaningtech.com/4.3/loader.js"
TURNSTILE_URL = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"


def sources() -> list[Path]:
    return [
        path
        for directory in SEARCH_ROOTS
        for path in (ROOT / directory).rglob("*")
        if path.is_file() and path.suffix in TEXT_SUFFIXES
    ]


def validate() -> list[str]:
    errors: list[str] = []
    mathjax_references = 0
    pyodide_references = 0
    for path in sources():
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for url in re.findall(r"https" + r"://[^\s'\"<>]+", source):
            if "mathjax@" in url:
                mathjax_references += 1
                if not (
                    url.startswith(MATHJAX_BASE)
                    or url == MATHJAX_BASE.removesuffix("/")
                    or url == MATHJAX_TEMPLATE_URL
                ):
                    errors.append(f"{relative}: MathJax sin versión canónica: {url}")
            if "pyodide/" in url and url.endswith("pyodide.mjs"):
                pyodide_references += 1
                if url != PYODIDE_URL:
                    errors.append(f"{relative}: Pyodide sin versión canónica: {url}")
        if "mathjax@3/es5" in source:
            errors.append(f"{relative}: referencia flotante mathjax@3")
        if "tex-svg.js" in source and MATHJAX_SRI not in source:
            errors.append(f"{relative}: carga de MathJax SVG sin integridad SRI")
    if mathjax_references < 8:
        errors.append("No se localizaron todas las cargas conocidas de MathJax")
    template = (ROOT / "docs/overrides/main.html").read_text(encoding="utf-8")
    if MATHJAX_TEMPLATE_URL not in template or "integrity=\"sha384-" not in template:
        errors.append("La plantilla principal no fija MathJax con integridad SRI")
    java_runtime = (ROOT / "docs/assets/javascripts/java-runtime.html").read_text(
        encoding="utf-8"
    )
    if CHEERPJ_URL not in java_runtime:
        errors.append("El ejecutor Java no usa la URL de CheerpJ permitida")
    site_script = (ROOT / "docs/assets/javascripts/site.js").read_text(encoding="utf-8")
    if TURNSTILE_URL not in site_script:
        errors.append("El formulario no usa la URL de Turnstile permitida")
    if pyodide_references != 1:
        errors.append(
            f"Se esperaba una carga explícita del ejecutor Pyodide; hay {pyodide_references}"
        )
    mathjax_site_config = (ROOT / "docs/assets/javascripts/mathjax.js").read_text(
        encoding="utf-8"
    )
    if "mtextInheritFont: true" not in mathjax_site_config:
        errors.append("docs/assets/javascripts/mathjax.js debe tener mtextInheritFont: true para renderizar tildes uniformes")
    tree_anim_source = (ROOT / "simulaciones/capitulo5/runtime/recursion_tree_animation.py").read_text(
        encoding="utf-8"
    )
    if "mtextInheritFont: true" not in tree_anim_source:
        errors.append("recursion_tree_animation.py debe configurar mtextInheritFont: true en MathJax SVG")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors))
        return 1
    print("Versiones exactas de MathJax y Pyodide validadas en recursos ejecutables.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
