import subprocess
import sys
import tomllib

import pytest

from moon_research.new_study import create_paper, create_study


def test_documentation_only_at_every_level(tmp_path):
    target = create_study("course/assignment-1", tmp_path)
    for node in (target, target.parent):
        assert (node / "README.md").is_file()
        assert (node / "docs/notes.md").is_file()
        assert not (node / "implementations").exists()
        assert not (node / "pyproject.toml").exists()
        assert not (node / ".venv").exists()


def test_independent_nested_environments(tmp_path):
    first = create_study("course/assignment-1", tmp_path, generate=True)
    second = create_study(
        "course/assignment-2",
        tmp_path,
        generate=True,
        languages=["cpp", "c", "typescript"],
    )
    config = tomllib.loads(
        (first / "implementations/python/pyproject.toml").read_text()
    )
    assert config["tool"]["uv"]["package"] is False
    assert not (first.parent / "pyproject.toml").exists()
    assert not (first / "implementations/python/.venv").exists()
    assert (second / "implementations/cpp/CMakeLists.txt").is_file()
    assert (second / "implementations/c/CMakeLists.txt").is_file()
    assert (second / "implementations/typescript/package.json").is_file()
    assert not (second / "implementations/python").exists()


def test_paper_routing_and_nested_docs(tmp_path):
    paper = create_paper("2017-attention/experiment-1", tmp_path)
    assert paper == tmp_path / "papers/2017-attention/experiment-1"
    assert not (tmp_path / "studies").exists()
    assert (paper / "docs/README.md").is_file()


def test_augment_preserves_user_work_and_rejects_overwrite(tmp_path):
    target = create_study("course", tmp_path)
    readme = target / "README.md"
    readme.write_text("My notes\n")
    create_study("course", tmp_path, generate=True)
    model = target / "implementations/python/src/model.py"
    model.write_text("user code\n")
    with pytest.raises(FileExistsError):
        create_study("course", tmp_path, generate=True, languages=["cpp", "python"])
    assert not (target / "implementations/cpp").exists()
    assert model.read_text() == "user code\n"
    create_study("course", tmp_path, generate=True, languages=["cpp"])
    assert readme.read_text() == "My notes\n"
    with pytest.raises(FileExistsError):
        create_study("course", tmp_path)


@pytest.mark.parametrize(
    "slug",
    [
        "../outside",
        "/absolute",
        "a//b",
        "a/../b",
        "a\\b",
        "Bad Name",
        "a/docs/b",
        "_template",
    ],
)
def test_rejects_unsafe_paths_without_writes(tmp_path, slug):
    with pytest.raises(ValueError):
        create_study(slug, tmp_path)
    assert not list(tmp_path.iterdir())


def test_rejects_symlink(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / "studies").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        create_study("course", tmp_path)
    assert not list(outside.iterdir())


@pytest.mark.parametrize(
    "kwargs",
    [
        {"languages": ["python"]},
        {"generate": True, "languages": ["rust"]},
        {"generate": True, "languages": []},
    ],
)
def test_invalid_options_do_not_write(tmp_path, kwargs):
    with pytest.raises(ValueError):
        create_study("course", tmp_path, **kwargs)
    assert not list(tmp_path.iterdir())


def test_cli_routes_and_rejects_removed_kind(tmp_path):
    for entry, collection in [("main", "studies"), ("paper_main", "papers")]:
        command = [
            sys.executable,
            "-c",
            f"from moon_research.new_study import {entry}; {entry}()",
        ]
        result = subprocess.run(
            command + ["course", "--root", str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert (tmp_path / collection / "course/README.md").is_file()
        result = subprocess.run(
            command + ["other", "--kind", "paper", "--root", str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2
        assert not (tmp_path / collection / "other").exists()
