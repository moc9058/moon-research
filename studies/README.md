# Studies

Each directory should answer one research question and remain independently
reproducible. Every study is its own uv project, with a local `pyproject.toml`,
`uv.lock`, and `.venv`. Prefer a small baseline and one informative comparison
over a large collection of unstructured notebooks.

Generate a directory with:

```bash
uv run new-study seq2seq_attention
cd studies/seq2seq_attention
uv sync --group dev
```

Then create or duplicate an Implementation record in Notion and link both ways.
