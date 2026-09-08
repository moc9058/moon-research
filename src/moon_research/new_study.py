"""Create a paper or topic study with isolated language projects."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUPPORTED_LANGUAGES = ("python", "c", "cpp", "typescript")

ROOT_README = """# {title}

Status: reading

## Source

- Exact title: TODO
- Authors: TODO
- Venue/year: TODO
- DOI/arXiv: TODO
- Notion record: TODO

## Research question

TODO

## Implementation status

| Language | Status | Notes |
| --- | --- | --- |
{language_rows}

## Reproduce

See each directory under `implementations/`.
"""

NOTES = """# Notes

## Summary

TODO

## Hypothesis

TODO

## Key idea

TODO

## Limitations

TODO

## Questions and connections

TODO
"""

PYPROJECT = """[project]
name = "moon-research-{slug}"
version = "0.1.0"
description = "Independent Python implementation for {title}"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["pytest>=8.3", "ruff>=0.9"]

[tool.uv]
package = false

[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
"""

CMAKE = """cmake_minimum_required(VERSION 3.25)
project({project_name} LANGUAGES {language})

enable_testing()
add_executable(main src/main.{extension})
add_test(NAME smoke COMMAND main)
"""

CMAKE_PRESETS = """{{
  "version": 6,
  "configurePresets": [{{
    "name": "default",
    "generator": "Ninja",
    "binaryDir": "${{sourceDir}}/build",
    "cacheVariables": {{"CMAKE_BUILD_TYPE": "Debug"}}
  }}],
  "buildPresets": [{{"name": "default", "configurePreset": "default"}}],
  "testPresets": [{{"name": "default", "configurePreset": "default"}}]
}}
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_python(root: Path, slug: str, title: str) -> None:
    write(root / "README.md", "# Python implementation\n\nRun `uv sync`.\n")
    write(root / ".python-version", "3.12\n")
    write(root / "pyproject.toml", PYPROJECT.format(slug=slug, title=title))
    write(root / "src" / ".gitkeep", "")
    write(
        root / "tests" / "test_smoke.py",
        "def test_placeholder() -> None:\n    assert True\n",
    )


def create_cmake(root: Path, slug: str, *, cpp: bool) -> None:
    language = "CXX" if cpp else "C"
    extension = "cpp" if cpp else "c"
    name = "C++" if cpp else "C"
    source = (
        "#include <iostream>\n\nint main() {\n"
        '    std::cout << "TODO: implement the paper\\n";\n    return 0;\n}\n'
        if cpp
        else "#include <stdio.h>\n\nint main(void) {\n"
        '    puts("TODO: implement the paper");\n    return 0;\n}\n'
    )
    write(root / "README.md", f"# {name} implementation\n\nUse CMake presets.\n")
    write(
        root / "CMakeLists.txt",
        CMAKE.format(
            project_name=slug.replace("-", "_"),
            language=language,
            extension=extension,
        ),
    )
    write(root / "CMakePresets.json", CMAKE_PRESETS.format())
    write(root / "src" / f"main.{extension}", source)
    write(root / "include" / ".gitkeep", "")


def create_typescript(root: Path, slug: str, title: str) -> None:
    package = {
        "name": f"moon-research-{slug}",
        "version": "0.1.0",
        "private": True,
        "description": f"Independent TypeScript implementation for {title}",
        "type": "module",
        "scripts": {"build": "tsc", "test": "npm run build && node dist/index.js"},
        "devDependencies": {"typescript": "^5.9.0"},
    }
    write(root / "README.md", "# TypeScript implementation\n\nRun `npm install`.\n")
    write(root / ".nvmrc", "22\n")
    write(root / "package.json", json.dumps(package, indent=2) + "\n")
    write(
        root / "tsconfig.json",
        '{\n  "compilerOptions": {\n    "target": "ES2022",\n'
        '    "module": "NodeNext",\n    "moduleResolution": "NodeNext",\n'
        '    "outDir": "dist",\n    "rootDir": "src",\n    "strict": true\n'
        '  },\n  "include": ["src/**/*.ts"]\n}\n',
    )
    write(root / "src" / "index.ts", 'console.log("TODO: implement the paper");\n')
    write(root / "tests" / ".gitkeep", "")


def create_study(
    slug: str,
    root: Path,
    *,
    kind: str = "study",
    languages: Iterable[str] = ("python",),
) -> Path:
    """Create a directory without overwriting existing work."""

    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError("Use lowercase kebab-case, such as seq2seq-attention.")
    if kind not in {"paper", "study"}:
        raise ValueError("kind must be 'paper' or 'study'.")
    selected = tuple(dict.fromkeys(languages))
    unsupported = set(selected) - set(SUPPORTED_LANGUAGES)
    if not selected or unsupported:
        raise ValueError(f"Choose one or more of: {', '.join(SUPPORTED_LANGUAGES)}.")

    destination = root / ("papers" if kind == "paper" else "studies") / slug
    destination.mkdir(parents=True, exist_ok=False)
    title = slug.replace("-", " ").title()
    rows = "\n".join(f"| {language} | planned | TODO |" for language in selected)
    write(
        destination / "README.md",
        ROOT_README.format(
            title=title,
            language_rows=rows,
        ),
    )
    write(destination / "docs" / "notes.md", NOTES)
    write(destination / "docs" / "derivations.md", "# Derivations\n\nTODO\n")
    write(destination / "docs" / "experiments.md", "# Experiments\n\nTODO\n")
    write(
        destination / "data" / "README.md",
        "# Data\n\nRecord source and preprocessing.\n",
    )
    write(destination / "results" / "README.md", "# Results\n\nIndex results here.\n")

    implementations = destination / "implementations"
    for language in selected:
        language_root = implementations / language
        if language == "python":
            create_python(language_root, slug, title)
        elif language == "c":
            create_cmake(language_root, slug, cpp=False)
        elif language == "cpp":
            create_cmake(language_root, slug, cpp=True)
        else:
            create_typescript(language_root, slug, title)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="lowercase kebab-case directory name")
    parser.add_argument("--kind", choices=("paper", "study"), default="study")
    parser.add_argument(
        "--languages", nargs="+", choices=SUPPORTED_LANGUAGES, default=["python"]
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    destination = create_study(
        args.slug,
        args.root,
        kind=args.kind,
        languages=args.languages,
    )
    print(f"Created {destination}")


if __name__ == "__main__":
    main()
