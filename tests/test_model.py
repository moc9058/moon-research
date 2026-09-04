from pathlib import Path


def test_starter_study_is_an_independent_uv_project() -> None:
    root = Path(__file__).resolve().parents[1]
    study = root / "studies" / "cnn_from_scratch"

    assert (study / "pyproject.toml").is_file()
    assert (study / "uv.lock").is_file()
    assert (study / ".python-version").is_file()
