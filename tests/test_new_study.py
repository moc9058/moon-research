from pathlib import Path

import pytest

from moon_research.new_study import create_study


def test_create_study(tmp_path: Path) -> None:
    destination = create_study("seq2seq_attention", tmp_path)

    assert destination == tmp_path / "studies" / "seq2seq_attention"
    assert (destination / "experiment.py").is_file()
    assert "Notion record: TODO" in (destination / "README.md").read_text()


def test_create_study_has_independent_uv_project(tmp_path: Path) -> None:
    destination = create_study("seq2seq_attention", tmp_path)

    pyproject = (destination / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "moon-research-seq2seq-attention"' in pyproject
    assert (destination / ".python-version").read_text(encoding="utf-8") == "3.12\n"
    assert (destination / "tests" / "test_smoke.py").is_file()


def test_create_study_rejects_unsafe_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        create_study("../outside", tmp_path)
