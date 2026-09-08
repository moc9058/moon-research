"""Create a paper or topic study with isolated language projects."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from collections.abc import Iterable
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUPPORTED_LANGUAGES = ("python", "c", "cpp", "typescript")

ROOT_README = """# {title}

Status: planned

## Goal and scope

TODO: course/topic, assignment, paper, or experiment; define this level's scope.

## Source

- Exact title / authors / venue / year: TODO
- Course / paper / DOI / arXiv URL: TODO
- Upstream code / exact revision / license: TODO
- Notion record: TODO

## Children

List child directories with relative links, purpose, and status. Keep each
child's details in its own README; link to shared parent notes where useful.

## Environment and implementation

This level starts as documentation only. If generated, see
`implementations/<language>/README.md` for independent setup commands.
Environment setup is not evidence of a completed implementation or reproduction.

## Notes

See [docs](docs/README.md). Research code is written by the user.
"""

DOCS_README = """# Documentation

Keep notes scoped to this level; link to parent/child documents instead of copying.

- [notes.md](notes.md): summary, hypothesis, key idea, limitations, questions.
- Add `derivations.md` when mathematical derivations are needed.
- Add `experiments.md` when experiments are planned: hypothesis, status, source
  revision, data version/split, working directory, command, configuration, seed,
  hardware, baseline, observations, artifact links, and limitations.
- Mark unrun experiments as **not run**. Record only observed results.
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
    write(root / "tests" / ".gitkeep", "")


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


def create_node(
    slug: str,
    root: Path,
    *,
    collection: str,
    generate: bool = False,
    languages: Iterable[str] | None = None,
) -> Path:
    """Create nested documentation nodes; opt in to isolated language scaffolds."""
    parts = slug.split("/")
    reserved = {"docs", "implementations", "data", "results", "src", "tests"}
    if any(not SLUG_PATTERN.fullmatch(p) or p in reserved for p in parts):
        raise ValueError(
            "Use slash-separated lowercase kebab-case names; "
            "docs/implementations/data/results/src/tests are reserved."
        )
    if collection not in {"papers", "studies"}:
        raise ValueError("Unknown collection.")
    if languages is not None and not generate:
        raise ValueError("--languages requires --generate.")
    selected = tuple(dict.fromkeys(languages if languages is not None else ("python",)))
    if generate and (not selected or set(selected) - set(SUPPORTED_LANGUAGES)):
        raise ValueError(f"Choose one or more of: {', '.join(SUPPORTED_LANGUAGES)}.")

    root = root.resolve()
    base = root / collection
    nodes = [base.joinpath(*parts[:i]) for i in range(1, len(parts) + 1)]
    destination = nodes[-1]
    # Validate every path before writing, including in-repository symlinks.
    candidates = [base, *nodes]
    if generate:
        candidates += [destination / "implementations"]
        candidates += [destination / "implementations" / lang for lang in selected]
    for path in candidates:
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f"Not a regular directory: {path}")
    if destination.exists() and not generate:
        raise FileExistsError(f"Already exists: {destination}")
    if generate:
        for lang in selected:
            target = destination / "implementations" / lang
            if target.exists():
                raise FileExistsError(f"Implementation already exists: {target}")

    # Stage new content so generator failures cannot leave half-written templates.
    with tempfile.TemporaryDirectory() as temporary:
        staging = Path(temporary)
        for node in nodes:
            if not node.exists():
                staged = staging / node.relative_to(root)
                title = node.name.replace("-", " ").title()
                write(staged / "README.md", ROOT_README.format(title=title))
                write(staged / "docs" / "README.md", DOCS_README)
                write(staged / "docs" / "notes.md", NOTES)
        for lang in selected if generate else ():
            staged = staging / destination.relative_to(root) / "implementations" / lang
            title = parts[-1].replace("-", " ").title()
            name = "-".join(parts)
            if lang == "python":
                create_python(staged, name, title)
                commands = (
                    "uv sync --group dev\n"
                    'uv run python -c "import sys; print(sys.executable)"'
                )
            elif lang in {"c", "cpp"}:
                create_cmake(staged, name, cpp=lang == "cpp")
                commands = (
                    "cmake --preset default\n"
                    "cmake --build --preset default\n"
                    "ctest --preset default"
                )
            else:
                create_typescript(staged, name, title)
                commands = "npm install --package-lock-only\nnpm ci\nnpm test"
            write(
                staged / "README.md",
                f"# {lang} implementation\n\n"
                f"Working directory: `{destination.relative_to(root)}/"
                f"implementations/{lang}/`\n\n"
                f"```bash\n{commands}\n```\n\n"
                "Generated configuration only; dependencies/builds have not run.\n"
                "Pin source-compatible versions, commit the resulting lockfile, and\n"
                "use locked installs thereafter. The user implements research "
                "code in `src/`.\n"
                "C/C++ and TypeScript programs are environment placeholders only.\n"
                "Add meaningful tests when there is behavior to verify.\n",
            )
            write(staged / "docs" / "README.md", DOCS_README)
            write(staged / "docs" / "notes.md", NOTES)
            write(
                staged / "data" / "README.md",
                "# Data\n\nRecord stable source URL, license, version/split, "
                "checksum if known,\nexpected local path, and access/preparation "
                "instructions. External links are valid.\n",
            )
            write(
                staged / "results" / "README.md",
                "# Results\n\nIndex external artifacts; record observations in "
                "../docs/experiments.md.\n",
            )
        files = list(staging.rglob("*"))
        for source in files:
            if source.is_file():
                target = root / source.relative_to(staging)
                if target.exists() or target.is_symlink():
                    raise FileExistsError(f"Refusing to overwrite: {target}")
        for source in files:
            if source.is_file():
                target = root / source.relative_to(staging)
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(source.read_text(encoding="utf-8"))
    return destination


def create_study(slug: str, root: Path, **kwargs) -> Path:
    return create_node(slug, root, collection="studies", **kwargs)


def create_paper(slug: str, root: Path, **kwargs) -> Path:
    return create_node(slug, root, collection="papers", **kwargs)


def run_cli(collection: str) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="relative path, e.g. course/assignment-1")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="add language configuration; does not install dependencies",
    )
    parser.add_argument("--languages", nargs="+", choices=SUPPORTED_LANGUAGES)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root (default: current directory)",
    )
    args = parser.parse_args()
    try:
        destination = create_node(
            args.slug,
            args.root,
            collection=collection,
            generate=args.generate,
            languages=args.languages,
        )
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f"Prepared {destination}")
    if args.generate:
        print(
            "Configuration generated. Follow "
            "implementations/<language>/README.md to install/build."
        )
    else:
        print("Documentation only; no implementation environment created.")


def main() -> None:
    run_cli("studies")


def paper_main() -> None:
    run_cli("papers")


if __name__ == "__main__":
    main()
