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
├── infra/aws/
│   ├── README.md                    # AWS rules and lifecycle
│   └── shared/README.md             # Default VM used by many papers
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
  --languages python cpp typescript \
  --compute shared
```

Create a topic study:

```bash
uv run new-study seq2seq-attention --languages python
```

The command never overwrites an existing directory.

Compute modes:

| Mode | Meaning | Files created |
| --- | --- | --- |
| `shared` | Use the repository-level AWS VM | README points to `infra/aws/shared/` |
| `dedicated` | Use a separate VM or topology | Creates `papers/<paper>/infra/aws/README.md` |
| `local` | Do not use AWS | README records local execution |

No AWS resource is currently deployed by this repository. Infrastructure
directories remain placeholders until requirements and a cost policy are
approved.

## Instructions for ChatGPT when adding a paper

When asked to set up a new paper, ChatGPT or another coding agent must read this
README and [docs/new-paper-workflow.md](docs/new-paper-workflow.md), then:

1. Inspect the repository and preserve unrelated user changes.
2. Collect or infer the year, slug, exact title, source URL, implementation
   languages, compute mode, and initial reproduction goal.
3. Default to `shared`. Choose `dedicated` only for isolation, multiple
   hosts, or special architecture, kernel, accelerator, or network needs.
4. Run `new-study`; do not invent a different directory structure.
5. Fill known metadata without fabricating unknown authors, links, or results.
6. Initialize language lockfiles where the required tool is available.
7. Add paper-specific AWS IaC only for `dedicated` mode. Never deploy cloud
   resources unless the user explicitly requests deployment.
8. Run repository tests and available language-level smoke checks.
9. Report paths, remaining TODOs, reproduction commands, and AWS deployment
   status.

The user can give ChatGPT this concise instruction:

> Set up this paper in moon-research using the repository workflow. Use
> [Python/C/C++/TypeScript] and [shared/dedicated/local] compute. Fill metadata
> from [PDF or URL], initialize the environments, run available checks, and
> commit the result. Do not deploy AWS resources.

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

## AWS compute model

The normal path is one shared EC2 VM for multiple papers:

```text
infra/aws/shared/                 # shared VM definition and operations
papers/<paper>/                   # paper code and documentation
└── docs/experiments.md           # commands run on the shared VM
```

If a paper cannot safely or reproducibly share that VM:

```text
papers/<paper>/infra/aws/         # dedicated VM or multi-VM topology
```

Commit infrastructure definitions, bootstrap scripts, tags, and lifecycle
commands. Do not commit credentials, private keys, account IDs, generated
state, instance IDs, or secrets. Every AWS environment must document
`deploy`, `connect`, `stop`, `status`, and `destroy`; `stop` and
`destroy` must remain visibly distinct.

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
