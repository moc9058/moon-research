# CNN From Scratch

Notion Implementation record: [CNN from Scratch — Starter Experiment](https://app.notion.com/p/3d169428c861812eae82f90a2201e8a2)

## Research question

Can a compact two-stage CNN overfit a small image dataset, and how do its
tensor shapes change from input to logits?

## Why this study comes first

It isolates convolution, pooling, channel growth, global average pooling, and
classification before moving to RNN, Seq2Seq, attention, and Transformers.

## Smoke run

The default configuration uses generated 32×32 RGB images. Its accuracy is not
scientifically meaningful; the run validates the data, training, evaluation,
and result-writing pipeline.

```bash
cd studies/cnn_from_scratch
uv sync --group dev
uv run pytest
uv run python train.py --config config.toml
```

This creates `studies/cnn_from_scratch/.venv`; it is separate from the
repository root and every other study.

To use CIFAR-10, duplicate the configuration and set `dataset = "cifar10"`.
Then remove the batch limits and increase the number of epochs.

## First meaningful experiments

1. Verify that the network can overfit 128 examples.
2. Remove the second convolution and compare capacity.
3. Replace global average pooling with a fully connected head.
4. Add normalization and compare learning curves.

Record the hypothesis before each run and link the result to the Notion entry.
