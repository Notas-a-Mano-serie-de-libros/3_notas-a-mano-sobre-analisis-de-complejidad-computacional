import re
import shlex
from pathlib import Path

from desarrollo.scripts.sync_local_execution import END, START, simulation_paths, sync

ROOT = Path(__file__).resolve().parents[2]


def notebook_commands(content):
    return {
        shlex.split(command)[2]
        for command in re.findall(r"`(jupyter lab [^`]+)`", content)
    }


def test_readme_opens_each_chapter_laboratory():
    content = (ROOT / "README.md").read_text()
    available = {f"simulaciones/capitulo{chapter}/notebooks/" for chapter in range(2, 9)}
    commands = re.findall(r"^jupyter lab (.+)$", content, re.MULTILINE)
    assert set(commands) == available
    assert len(commands) == 7
    assert all((ROOT / directory).is_dir() for directory in commands)
    assert "<details>" not in content
    assert re.findall(r"^## (.+)$", content, re.MULTILINE) == [
        "Complemento digital de la obra",
        "Inicio rápido",
        "Compatibilidad verificada",
        "Guía de instalación",
        "Guía de ejecución de animaciones por capítulo",
    ]
    assert not list((ROOT / "simulaciones").rglob("README.md"))


def test_every_colab_link_has_its_matching_local_command():
    assert sync(check=True) == []
    for path in (ROOT / "docs").rglob("*.md"):
        content = path.read_text()
        notebooks = simulation_paths(content)
        if not notebooks:
            continue
        assert content.count(START) == content.count(END) == 1, path
        chapters = {Path(notebook).parts[1] for notebook in notebooks}
        expected = ({f"simulaciones/{chapter}/notebooks/" for chapter in chapters}
                    if chapters <= {"capitulo7", "capitulo8"} else set(notebooks))
        assert notebook_commands(content) == expected, path
        assert all((ROOT / notebook).is_file() for notebook in notebooks), path
