from pathlib import Path

import pytest

from moon_research.new_study import create_study


def test_create_paper_with_selected_languages(tmp_path: Path) -> None:
    destination = create_study(
        "2017-attention-is-all-you-need",
        tmp_path,
        kind="paper",
        languages=("python", "cpp", "typescript"),
    )

    assert destination == tmp_path / "papers" / "2017-attention-is-all-you-need"
    assert (destination / "docs" / "notes.md").is_file()
    assert (destination / "implementations" / "python" / "pyproject.toml").is_file()
    assert (destination / "implementations" / "cpp" / "CMakeLists.txt").is_file()
    assert (destination / "implementations" / "typescript" / "package.json").is_file()
    assert not (destination / "implementations" / "c").exists()
    assert not (destination / "infra").exists()


def test_python_is_an_independent_uv_project(tmp_path: Path) -> None:
    destination = create_study("seq2seq-attention", tmp_path)
    python = destination / "implementations" / "python"

    pyproject = (python / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "moon-research-seq2seq-attention"' in pyproject
    assert (python / ".python-version").read_text(encoding="utf-8") == "3.12\n"
    assert (python / "tests" / "test_smoke.py").is_file()


def test_rejects_unsafe_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        create_study("../outside", tmp_path)


def test_rejects_unknown_language(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        create_study("valid-name", tmp_path, languages=("rust",))
