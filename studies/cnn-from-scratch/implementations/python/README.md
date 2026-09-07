# Python implementation

```bash
uv sync --locked --group dev
uv run pytest
uv run python train.py --config config.toml
```

Generated results are written under `results/`; downloaded data is stored under
`data/`. Both are ignored except for their README files.
