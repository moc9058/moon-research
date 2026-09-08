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

A paper or study owns its documentation, data description, results, and all
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

## Instructions for Codex: papers and studies

Read `AGENTS.md`, this README, and
[the setup workflow](docs/new-paper-workflow.md) before adding or updating either
`papers/` or `studies/`. The default request is **environment setup only**.
The user writes the research code.

| Responsibility | Default owner |
| --- | --- |
| Directories, dependency manifests, lockfiles, environment instructions | Codex |
| Source metadata, upstream version, dataset links and local path instructions | Codex |
| Import/build checks and small environment smoke checks | Codex |
| Models, algorithms, training/evaluation loops, research preprocessing, experimental changes | User |
| Long training runs, bulk downloads, cloud provisioning | Only when explicitly requested |

Codex must:

1. Inspect the target directory and preserve existing code and unrelated changes.
   Use `new-study` only for a new target; update an existing project in place.
2. Choose `papers/` for one paper and `studies/` for a topic, tutorial, or exercise.
   Infer routine details; ask only for missing information that changes setup.
3. Record the goal: upstream reproduction, independent implementation, or a
   modification experiment. Identify the target table, figure, metric, or behavior.
4. Prepare only the requested languages and dependencies justified by the source
   or user's plan. Check Python/framework/OS/CPU/GPU compatibility rather than
   blindly retaining the generator's default versions.
5. Leave research implementation to the user. Empty source directories, TODO
   placeholders, configuration files, and setup scripts are allowed. Do not
   implement or alter research logic without a specific request.
6. Record the upstream repository URL and exact commit/tag. Keep upstream code
   separate from user code; document its license and original commands.
7. Document datasets using stable external links, versions, splits, expected
   local paths, and download/access instructions. Do not commit dataset files,
   checkpoints, credentials, or signed download URLs.
8. Verify only what is available: environment/build checks are not scientific
   reproduction. Mark unrun commands and missing data/hardware explicitly.
9. Report changed files, checks, exact next commands with working directories,
   the first file the user should implement, and outstanding limitations.

Detailed source/data rules, baseline records, and reusable Korean request
examples are in [docs/new-paper-workflow.md](docs/new-paper-workflow.md).

A short request is sufficient:

> Set up [paper URL / study topic] in moon-research using the repository workflow.
> My goal is [upstream reproduction / own implementation / modification].
> Use [language] on [OS, CPU/GPU]. I will write the research code; prepare the
> environment, source/data references, and verification instructions only.

## Independent environments

Isolation is per paper/study and per language:

| Language | Files committed | Generated locally |
| --- | --- | --- |
| Python | `pyproject.toml`, `uv.lock`, `.python-version` | `.venv/` |
| C | `CMakeLists.txt`, `CMakePresets.json` | `build/` |
| C++ | `CMakeLists.txt`, `CMakePresets.json` | `build/` |
| TypeScript | `package.json`, `package-lock.json`, `.nvmrc` | `node_modules/`, `dist/` |

Do not make paper/study projects members of one uv or npm workspace. Separate
lockfiles allow projects to use conflicting dependency versions. CMake keeps
build settings and outputs separate. Add a paper-level `.devcontainer/` only
when compiler, OS, CUDA, or system-library versions must also be pinned.

## Run implementation checks

Run these inside the relevant `implementations/<language>/` directory.
These are environment/build checks; generated placeholder tests do not establish
algorithm correctness or reproduction of a paper.

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

## Paper and study documentation

| File | Purpose |
| --- | --- |
| `README.md` | Bibliographic metadata, research question, status, links |
| `docs/notes.md` | Summary, hypothesis, key idea, limitations, questions |
| `docs/derivations.md` | Mathematical derivations and prerequisites |
| `docs/experiments.md` | Commands, configurations, results, interpretation |
| `data/README.md` | Data source, license, download and preprocessing |
| `results/README.md` | Small committed results and large external artifacts |

Each language-level `README.md` explains setup, commands, implementation scope,
and known differences from the source. `data/README.md` can contain external
links only: data does not need to live in Git or be downloaded during setup.

The default ignore rules keep only `data/README.md` and `results/README.md` from
those directories. Put experiment records in `docs/experiments.md`; index large
results with external links in `results/README.md`. If small reviewed metrics
files should be committed, add a narrow ignore exception for those files.

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
