"""Create a consistent directory for a new model or paper study."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

README_TEMPLATE = """# {title}

Notion record: TODO

## Research question

TODO

## Source

- Paper/resource: TODO
- Concepts: TODO

## Hypothesis

TODO

## Reproduce

```bash
cd studies/{slug}
uv sync --group dev
uv run python experiment.py
```

## Results

| Run | Commit | Configuration | Metric | Interpretation |
| --- | --- | --- | --- | --- |
| 001 | TODO | `config.toml` | TODO | TODO |

## Failures and lessons

TODO
"""

PYPROJECT_TEMPLATE = """[project]
name = "moon-research-{project_name}"
version = "0.1.0"
description = "Independent Moon Research study: {title}"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.3",
    "ruff>=0.9",
]

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

EXPERIMENT_TEMPLATE = '''"""Entry point for the {slug} study."""


def main() -> None:
    """Run the smallest meaningful experiment."""
    raise NotImplementedError("Define the experiment and success criterion first.")


if __name__ == "__main__":
    main()
'''

CONFIG_TEMPLATE = """[experiment]
seed = 42
"""

TEST_TEMPLATE = '''"""Starter test for the {slug} study."""


def test_placeholder() -> None:
    """Replace this with the study's first meaningful invariant."""
    assert True
'''


def create_study(slug: str, root: Path) -> Path:
    """Create a study package without overwriting existing work."""

    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            "Use a Python-safe snake_case slug, such as seq2seq_attention."
        )

    destination = root / "studies" / slug
    destination.mkdir(parents=True, exist_ok=False)
    title = slug.replace("_", " ").title()
    (destination / "tests").mkdir()
    (destination / "results").mkdir()
    (destination / ".python-version").write_text("3.12\n", encoding="utf-8")
    (destination / "pyproject.toml").write_text(
        PYPROJECT_TEMPLATE.format(project_name=slug.replace("_", "-"), title=title),
        encoding="utf-8",
    )
    (destination / "__init__.py").write_text("", encoding="utf-8")
    (destination / "README.md").write_text(
        README_TEMPLATE.format(title=title, slug=slug), encoding="utf-8"
    )
    (destination / "config.toml").write_text(CONFIG_TEMPLATE, encoding="utf-8")
    (destination / "experiment.py").write_text(
        EXPERIMENT_TEMPLATE.format(slug=slug), encoding="utf-8"
    )
    (destination / "tests" / "test_smoke.py").write_text(
        TEST_TEMPLATE.format(slug=slug), encoding="utf-8"
    )
    (destination / "results" / "README.md").write_text(
        "# Results\n\nGenerated outputs belong here and are ignored by Git.\n",
        encoding="utf-8",
    )
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="Python-safe snake_case study name")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root; defaults to the current directory",
    )
    args = parser.parse_args()
    destination = create_study(args.slug, args.root)
    print(f"Created {destination}")


if __name__ == "__main__":
    main()
