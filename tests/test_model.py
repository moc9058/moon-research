from pathlib import Path


def test_starter_study_is_an_independent_uv_project() -> None:
    root = Path(__file__).resolve().parents[1]
    implementation = (
        root / "studies" / "cnn-from-scratch" / "implementations" / "python"
    )

    assert (implementation / "pyproject.toml").is_file()
    assert (implementation / "uv.lock").is_file()
    assert (implementation / ".python-version").is_file()
