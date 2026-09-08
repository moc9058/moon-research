# New paper workflow

This is the canonical procedure for a human or coding agent adding a paper.

## Required inputs

| Input | Example | Default |
| --- | --- | --- |
| Paper source | PDF, DOI, arXiv URL | Required |
| Directory slug | `2017-attention-is-all-you-need` | Infer from year and title |
| Languages | `python cpp` | `python` |
| Initial goal | Read, reproduce, benchmark, extend | Read and create a smoke test |

Ask one concise question only when a missing input would materially change the
layout. Unknown bibliographic details may remain TODO; never invent them.

## Create

```bash
uv sync --locked --group dev

uv run new-study <year-short-title> \
  --kind paper \
  --languages <language...>
```

Populate the generated paper README from the source and record the initial
reading notes. Keep code under `implementations/<language>/`, not in the paper
root.

## Initialize environments

- Python: run `uv lock`, then `uv sync --locked --group dev`.
- TypeScript: run `npm install --package-lock-only`, then `npm ci`.
- C/C++: validate `CMakePresets.json`, configure, build, and run CTest when
  CMake and a compiler are available.

Do not add large frameworks speculatively. Dependencies should follow the first
implementation or reproduction goal.

## Complete the paper README

Record:

- exact title, authors, venue/year, DOI or arXiv link, and Notion link;
- research question, intended reproduction boundary, and current status;
- selected languages and their status;
- exact setup, test, and experiment commands;
- known differences from the original paper.

## Verification and handoff

Before committing:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest
git diff --check
```

Also run each initialized language's smallest smoke check. In the handoff,
report created paths, checks and outcomes, unresolved TODOs, and next commands.
