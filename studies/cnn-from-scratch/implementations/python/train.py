"""Train the starter CNN on generated data or CIFAR-10."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms

from experiment import (
    ExperimentConfig,
    load_config,
    save_run,
    seed_everything,
)
from model import SmallCNN

STUDY_ROOT = Path(__file__).resolve().parent


def build_datasets(config: ExperimentConfig) -> tuple[Dataset, Dataset]:
    transform = transforms.ToTensor()
    if config.dataset == "fake":
        train_set = datasets.FakeData(
            size=config.train_samples,
            image_size=(3, 32, 32),
            num_classes=10,
            transform=transform,
            random_offset=config.seed,
        )
        test_set = datasets.FakeData(
            size=config.test_samples,
            image_size=(3, 32, 32),
            num_classes=10,
            transform=transform,
            random_offset=config.seed + config.train_samples,
        )
        return train_set, test_set
    if config.dataset == "cifar10":
        data_root = STUDY_ROOT / config.data_dir
        return (
            datasets.CIFAR10(data_root, train=True, download=True, transform=transform),
            datasets.CIFAR10(
                data_root, train=False, download=True, transform=transform
            ),
        )
    raise ValueError(f"Unsupported dataset: {config.dataset!r}")


def limited_batches(
    loader: DataLoader, maximum: int | None
) -> Iterable[tuple[torch.Tensor, torch.Tensor]]:
    for index, batch in enumerate(loader):
        if maximum is not None and index >= maximum:
            break
        yield batch


def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    maximum_batches: int | None,
) -> float:
    model.train()
    total_loss = 0.0
    batches = 0
    for inputs, targets in limited_batches(loader, maximum_batches):
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        loss = criterion(model(inputs), targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        batches += 1
    return total_loss / max(batches, 1)


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    maximum_batches: int | None,
) -> float:
    model.eval()
    correct = 0
    total = 0
    for inputs, targets in limited_batches(loader, maximum_batches):
        predictions = model(inputs.to(device)).argmax(dim=1).cpu()
        correct += int((predictions == targets).sum())
        total += targets.numel()
    return correct / max(total, 1)


def run(config: ExperimentConfig) -> dict[str, float | str]:
    seed_everything(config.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_set, test_set = build_datasets(config)
    generator = torch.Generator().manual_seed(config.seed)
    train_loader = DataLoader(
        train_set,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
        generator=generator,
    )
    test_loader = DataLoader(
        test_set,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
    )

    model = SmallCNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()
    loss = 0.0
    for _ in range(config.epochs):
        loss = train_epoch(
            model,
            train_loader,
            optimizer,
            criterion,
            device,
            config.max_train_batches,
        )
    accuracy = evaluate(model, test_loader, device, config.max_test_batches)
    return {"device": str(device), "final_train_loss": loss, "test_accuracy": accuracy}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=STUDY_ROOT / "config.toml",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=STUDY_ROOT / "results" / "latest.json",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    metrics = run(config)
    save_run(args.output, config, metrics)
    print(metrics)
    print(f"Saved run to {args.output}")


if __name__ == "__main__":
    main()
