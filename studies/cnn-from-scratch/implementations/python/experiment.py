"""Configuration, reproducibility, and lightweight result tracking."""

from __future__ import annotations

import json
import random
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch


@dataclass(frozen=True)
class ExperimentConfig:
    """Small, explicit configuration for the starter CNN experiment."""

    seed: int = 42
    dataset: str = "fake"
    data_dir: str = "data"
    epochs: int = 1
    batch_size: int = 32
    learning_rate: float = 1e-3
    num_workers: int = 0
    train_samples: int = 256
    test_samples: int = 128
    max_train_batches: int | None = 4
    max_test_batches: int | None = 2


def load_config(path: str | Path) -> ExperimentConfig:
    """Load an experiment configuration from a TOML file."""

    with Path(path).open("rb") as file:
        raw = tomllib.load(file)
    values = raw.get("experiment", raw)
    return ExperimentConfig(**values)


def seed_everything(seed: int) -> None:
    """Seed common random-number generators for repeatable experiments."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def save_run(
    output_path: str | Path,
    config: ExperimentConfig,
    metrics: dict[str, Any],
) -> None:
    """Persist configuration and metrics as one reviewable JSON document."""

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {"config": asdict(config), "metrics": metrics}
    destination.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
