# Moon Research

A reproducible workspace for learning AI by reading papers, implementing models,
and recording experiments. Notion holds the knowledge graph; this repository
holds executable evidence.

## Start here

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Create the lightweight repository-tools environment:

   ```bash
   uv sync --group dev
   ```

3. Run the test suite:

   ```bash
   uv run pytest
   ```

4. Create a separate environment for the included CNN study:

   ```bash
   cd studies/cnn_from_scratch
   uv sync --group dev
   uv run pytest
   uv run python train.py
   ```

   The generated-image smoke run does not require a dataset download.

5. Create a new study:

   ```bash
   cd ../..
   uv run new-study seq2seq_attention
   cd studies/seq2seq_attention
   uv sync --group dev
   ```

## Independent environments

The root tooling and every implementation are separate uv projects. Each
directory owns its `pyproject.toml`, `uv.lock`, and `.venv`:

| Project | Environment | Purpose |
| --- | --- | --- |
| Repository root | `moon-research/.venv` | Scaffolding, lint, and root tests |
| CNN study | `studies/cnn_from_scratch/.venv` | PyTorch, torchvision, and CNN tests |
| Future study | `studies/<study>/.venv` | Only that implementation's dependencies |

Run uv from inside a study directory, or use `uv --project studies/<study> ...`
from the repository root. Dependencies installed for one implementation do not
enter another implementation's environment.

## Notion knowledge graph

Use the [moon-research Notion hub](https://app.notion.com/p/3d169428c8618198a261c0f821b25f98)
for reading notes and relationships. The active system intentionally has only
two databases:

- **Articles**: one node per paper, survey, article, or technical document.
- **Links**: directed, typed edges between Articles, with rationale and evidence.

Duplicate `TEMPLATE — Article note (duplicate me)` when processing a source.
See [docs/notion-workflow.md](docs/notion-workflow.md) for the complete workflow.

## Repository layout

```text
moon-research/
├── docs/                     # Workflow and research documentation
├── src/moon_research/        # Lightweight repository tooling
├── studies/                  # One uv project per implementation/reproduction
│   ├── _template/            # Reference layout for a new study
│   └── cnn_from_scratch/     # Runnable starter study
├── tests/                    # Fast tests for repository tooling
└── .github/workflows/        # Continuous integration
```

## Working agreement

For every experiment, commit:

- the research question;
- the configuration and random seed;
- the exact command;
- a small machine-readable metrics file;
- failures and interpretation, not just the successful result;
- a link to the matching Notion Article.

Do not commit paper PDFs, private company data, datasets, model checkpoints,
secrets, or generated caches. Store only download instructions and provenance.

Repository: [moc9058/moon-research](https://github.com/moc9058/moon-research)

After committing an implementation, paste its directory or commit URL into the
Article's `GitHub URL` property in Notion.
