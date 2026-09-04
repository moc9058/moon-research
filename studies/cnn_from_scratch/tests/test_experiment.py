from __future__ import annotations

import json
from pathlib import Path

from experiment import ExperimentConfig, load_config, save_run


def test_load_smoke_config() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_config(root / "config.toml")

    assert config.dataset == "fake"
    assert config.seed == 42
    assert config.max_train_batches == 4


def test_save_run(tmp_path: Path) -> None:
    destination = tmp_path / "nested" / "metrics.json"
    save_run(destination, ExperimentConfig(), {"accuracy": 0.5})

    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload["config"]["seed"] == 42
    assert payload["metrics"]["accuracy"] == 0.5
