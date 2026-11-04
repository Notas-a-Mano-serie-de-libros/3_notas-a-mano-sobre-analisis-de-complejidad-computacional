from desarrollo.scripts import validate_external_references, validate_repository_paths


def test_repository_path_scan_skips_generated_and_dependency_directories(
    tmp_path, monkeypatch
):
    source = tmp_path / "docs" / "index.md"
    source.parent.mkdir()
    source.write_text("[missing](missing.md)", encoding="utf-8")
    for directory in ("node_modules", "site", "build", "dist"):
        generated = tmp_path / directory / "README.md"
        generated.parent.mkdir()
        generated.write_text("[missing](missing.md)", encoding="utf-8")

    monkeypatch.setattr(validate_repository_paths, "PROJECT_ROOT", tmp_path)

    assert validate_repository_paths.repository_files() == [source]
    errors = validate_repository_paths.validate_repository_paths()
    assert errors == ["docs/index.md enlaza un destino inexistente: missing.md"]


def test_external_reference_scan_skips_generated_and_dependency_directories(
    tmp_path,
):
    malformed_url = "https:" + "/" + "/[not-ipv6/path"
    local_url = "http:" + "/" + "/localhost:8000"
    source = tmp_path / "source.py"
    source.write_text(f'malformed = "{malformed_url}"\nlocal = "{local_url}"\n',
        encoding="utf-8",
    )
    for directory in ("node_modules", "site", "build", "dist"):
        generated = tmp_path / directory / "README.md"
        generated.parent.mkdir()
        generated.write_text(f'url = "{local_url}"\n', encoding="utf-8")

    errors, count = validate_external_references.validate(tmp_path)

    assert count == 2
    assert errors == [
        f"source.py: URL malformada: {malformed_url}",
        f"source.py: URL no segura: {local_url}",
        f"source.py: URL local publicada: {local_url}",
    ]
