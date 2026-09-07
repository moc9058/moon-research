# Moon Research

A reproducible repository for reading papers, implementing ideas in multiple
languages, and recording experiments.

## Repository layout

```text
moon-research/
├── papers/                         # One directory per paper
│   └── 2017-attention-is-all-you-need/
│       ├── README.md               # Metadata, question, status, links
│       ├── docs/                   # Notes, derivations, experiment log
│       ├── implementations/
│       │   ├── python/             # pyproject.toml + uv.lock + .venv
│       │   ├── cpp/                # CMakeLists.txt + presets + build
│       │   ├── c/                  # CMakeLists.txt + presets + build
│       │   └── typescript/         # package.json + lock + node_modules
│       ├── data/README.md           # Data provenance; data is ignored
│       └── results/README.md        # Small, reviewable results
├── studies/                        # Work not tied to one paper
│   └── cnn-from-scratch/
│       ├── README.md
│       ├── docs/
│       └── implementations/python/
├── src/moon_research/              # Repository scaffolding tools
├── tests/                          # Tests for repository tooling
└── .github/workflows/              # Continuous integration
```

A paper owns its documentation, data description, results, and all
implementations. Create only the language directories that it actually uses.

## Naming

- Paper: `<year>-<short-title>`, such as `2017-attention-is-all-you-need`.
- Study: lowercase kebab-case, such as `cnn-from-scratch`.
- Python import packages: snake_case inside `src/`.

Keep the exact title, authors, venue, DOI/arXiv URL, and Notion URL in each
paper's `README.md`.

## Create a paper or study

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and set up
the lightweight root tooling:

```bash
uv sync --group dev
```

Create a paper with only the implementations you need:

```bash
uv run new-study 2017-attention-is-all-you-need \
  --kind paper \
  --languages python cpp typescript
```

Create a topic study:

```bash
uv run new-study seq2seq-attention --languages python
```

The command never overwrites an existing directory.

## Independent environments

Isolation is per paper and per language:

| Language | Files committed | Generated locally |
| --- | --- | --- |
| Python | `pyproject.toml`, `uv.lock`, `.python-version` | `.venv/` |
| C | `CMakeLists.txt`, `CMakePresets.json` | `build/` |
| C++ | `CMakeLists.txt`, `CMakePresets.json` | `build/` |
| TypeScript | `package.json`, `package-lock.json`, `.nvmrc` | `node_modules/`, `dist/` |

Do not make paper projects members of one uv or npm workspace. Separate
lockfiles allow papers to use conflicting dependency versions. CMake keeps
build settings and outputs separate. Add a paper-level `.devcontainer/` only
when compiler, OS, CUDA, or system-library versions must also be pinned.

Example commands:

```bash
# Python
uv sync --locked --group dev && uv run pytest

# C or C++
cmake --preset default
cmake --build --preset default
ctest --preset default

# TypeScript
npm ci && npm test
```

## Paper documentation

| File | Purpose |
| --- | --- |
| `README.md` | Bibliographic metadata, research question, status, links |
| `docs/notes.md` | Summary, hypothesis, key idea, limitations, questions |
| `docs/derivations.md` | Mathematical derivations and prerequisites |
| `docs/experiments.md` | Commands, configurations, results, interpretation |
| `data/README.md` | Data source, license, download and preprocessing |
| `results/README.md` | Small committed results and large external artifacts |

Each language-level `README.md` explains setup, commands, implementation scope,
and known differences from the paper.

## Included CNN study

```bash
cd studies/cnn-from-scratch/implementations/python
uv sync --locked --group dev
uv run pytest
uv run python train.py --config config.toml
```

The generated-data smoke run validates the training and result-writing pipeline
without downloading a dataset.

## Notion article library

Use the [moon-research Notion hub](https://app.notion.com/p/3d169428c8618198a261c0f821b25f98)
for article files and concise knowledge-graph records. Keep executable code and
experiment evidence here. See [docs/notion-workflow.md](docs/notion-workflow.md).

## Working agreement

For every experiment, record:

- the question and hypothesis before running it;
- the exact command, configuration, seed, and language;
- a small machine-readable metrics file when useful;
- failures and interpretation, not only successful results;
- differences from the original paper.

Do not commit paper PDFs, private company data, downloaded datasets, model
checkpoints, secrets, virtual environments, dependency directories, or build
outputs.

Repository: [moc9058/moon-research](https://github.com/moc9058/moon-research)
