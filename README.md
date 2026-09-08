# Moon Research

A reproducible repository for reading papers, implementing ideas in multiple
languages, and recording experiments.

## Repository layout

| Path | Role |
| --- | --- |
| `papers/<paper>/README.md`, `docs/` | Paper scope, sources, notes, child links |
| `papers/<paper>/<experiment>/README.md`, `docs/` | Optional nested experiment |
| `studies/<course>/README.md`, `docs/` | Course container without an environment |
| `studies/<course>/<assignment>/README.md`, `docs/` | Assignment scope and notes |
| `<node>/implementations/<language>/` | Optional independent language environment |
| `src/moon_research/` | Repository scaffolding commands |
| `tests/` | Tests for repository tooling |
| `.github/workflows/` | Continuous integration |

`<node>` is any paper/study/assignment/experiment path. Hierarchy depth does
not determine whether a node needs an environment; its execution needs do.


A paper, course, assignment, or experiment owns its documentation. Containers
need no environment. Executable nodes keep independent language projects under
`implementations/`, including their data/result descriptions. Create only needed languages.

## Naming

- Paper: `<year>-<short-title>`, such as `2017-attention-is-all-you-need`.
- Study and nested nodes: lowercase kebab-case, such as `course/assignment-1`.
- Python import packages: snake_case inside `src/`.

Keep the exact title, authors, venue, DOI/arXiv URL, and Notion URL in each
paper's `README.md`.

## Create a paper or study

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and set up
the lightweight root tooling:

```bash
uv sync --group dev
```

`uv sync --group dev` creates/updates the root `.venv`, installs this repository's
CLI tools (`new-study`, `new-paper`) and the `dev` group (`pytest`, `ruff`). It
uses `uv.lock`, updating the lock if needed. Use `--locked` to reject stale locks.
The root environment is only for repository tools; it does not install child
projects. `dev` is included by default in uv; the explicit flag makes intent clear.
`uv run` also syncs automatically, so a separate initial sync is convenient but
not required. See [uv syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

Run generation commands from the repository root:

```bash
# Documentation containers: README.md + docs/, no language environment
uv run new-study stanford-cs-224n-spring-2024
uv run new-paper 2017-attention-is-all-you-need

# Nested assignments with different, independent language configurations
uv run new-study stanford-cs-224n-spring-2024/assignment-1 --generate --languages python
uv run new-study stanford-cs-224n-spring-2024/assignment-2 --generate --languages cpp

# Add an environment to the existing paper container
uv run new-paper 2017-attention-is-all-you-need --generate --languages python
```

`new-study` always targets `studies/`; `new-paper` always targets `papers/`.
`--kind` has been removed. Both commands default to documentation only.
`--generate` adds configuration under `implementations/<language>/`; its default
language is Python. `--languages` requires `--generate`.

Nested paths can have arbitrary depth. Each missing ancestor receives its own
README and docs. Use kebab-case paths such as `assignment-1`; the README title
can say “Assignment 1”. Reserved infrastructure names (`docs`, `implementations`,
`data`, `results`, `src`, `tests`) cannot be hierarchy components.
Use `--root /path/to/moon-research` to select the destination explicitly.

Existing documentation is preserved. An existing node can receive a new language
with `--generate`; an existing language directory is rejected without overwriting
files. For dependency changes in an existing implementation, edit it in place.
Repeating a documentation-only creation also reports that the directory exists.

Generation does **not** install packages or create `.venv`. Initialize Python
only in the selected implementation directory:

```bash
cd studies/stanford-cs-224n-spring-2024/assignment-1/implementations/python
uv sync --group dev
# Commit the resulting uv.lock; subsequent installs use:
uv sync --locked --group dev
```

Do not run study environment setup from a course/assignment documentation folder:
uv can discover the root project in its parents. Each actual language project
owns its environment; siblings and parent containers do not share it.

## Why src/moon_research and tests exist

`src/moon_research/` implements the installed generator commands. Deleting it
would break `uv run new-study` and `uv run new-paper`. Root `tests/` checks nested
paths, routing, environment isolation, and preservation of existing files.
They are repository tooling, not a place for paper or assignment implementations.
Keep both while using these commands. Research tests belong to their own
`implementations/<language>/tests/` directory. No always-passing placeholder
Python tests are generated.

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
   Use `new-study` or `new-paper` for new nodes; use `--generate` only to add a missing language. Update existing implementations in place.
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

Isolation is per executable node (including nested assignments/experiments) and per language:

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
These are environment/build checks; they do not establish algorithm correctness
or reproduction of a paper. New Python scaffolds contain no tests yet; run pytest
only after meaningful tests have been added.

Example commands:

```bash
# Python
uv sync --locked --group dev
uv run python -c "import sys; print(sys.executable)"

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

At every course/paper/assignment/experiment level, create `README.md`,
`docs/README.md`, and `docs/notes.md`. README records scope, sources, status,
relative child links, and environment ownership. Codex updates the parent child
index when adding a node; the generator leaves existing README content untouched.
Add derivations and experiment logs only when relevant. Put shared concepts at
the parent and assignment-specific notes at the child; link instead of duplicating.
Language projects also receive README/docs. `data/` and `results/` documentation
is generated inside language projects; shared data may be documented at a parent.
The same documentation templates are in `studies/_template` and `papers/_template`.

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
