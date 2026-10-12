from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_pages_permissions_are_scoped_per_job():
    workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    top_level = workflow.split("jobs:", 1)[0]
    build_job = workflow.split("  build:\n", 1)[1].split("  deploy:\n", 1)[0]
    deploy_job = workflow.split("  deploy:\n", 1)[1]
    assert "contents: read" in top_level
    assert "pages: write" not in top_level
    assert "id-token: write" not in top_level
    assert "pages: write" not in build_job
    assert "id-token: write" not in build_job
    assert "pages: write" in deploy_job
    assert "id-token: write" in deploy_job


def test_legacy_laboratories_are_not_published_twice():
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    excluded = mkdocs.split("exclude_docs:", 1)[1].split("markdown_extensions:", 1)[0]
    assert "laboratorios/" in excluded


def test_colab_label_is_canonical_in_documentation():
    offenders = []
    for path in (ROOT / "docs").rglob("*.md"):
        if "Abrir en Google Colab" in path.read_text(encoding="utf-8"):
            offenders.append(path.relative_to(ROOT).as_posix())
    assert offenders == []


def test_python_minimum_is_consistent():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "Python-3.11%2B" in readme
    assert "Python | 3.11 o superior" in readme
    assert 'target-version = "py311"' in pyproject
    assert '"3.11"' in ci and '"3.12"' in ci
    assert '"3.10"' not in ci
