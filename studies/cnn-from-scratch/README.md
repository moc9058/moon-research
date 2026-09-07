# CNN From Scratch

Notion record: [CNN from Scratch — Starter Experiment](https://app.notion.com/p/3d169428c861812eae82f90a2201e8a2)

## Research question

Can a compact two-stage CNN overfit a small image dataset, and how do its tensor
shapes change from input to logits?

## Documentation

- [Notes](docs/notes.md)
- [Experiment log](docs/experiments.md)
- [Python implementation](implementations/python/README.md)

## Reproduce

```bash
cd studies/cnn-from-scratch/implementations/python
uv sync --locked --group dev
uv run pytest
uv run python train.py --config config.toml
```

The local `.venv` and dependencies belong only to this implementation.
