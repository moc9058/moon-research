# Studies

Use this area for concept implementations not tied to one paper. A study follows
the paper layout: documentation at the study level and independent projects
under `implementations/`.

```bash
uv run new-study seq2seq-attention --languages python
cd studies/seq2seq-attention/implementations/python
uv sync --group dev
```

For Codex setup, follow [the paper/study workflow](../docs/new-paper-workflow.md).
The user writes research code; prepare environments and source/data references only
unless implementation is explicitly requested. Large datasets may remain external links.
