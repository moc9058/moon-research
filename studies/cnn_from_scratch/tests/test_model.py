import torch

from model import SmallCNN


def test_cnn_output_shape() -> None:
    model = SmallCNN(input_channels=3, num_classes=10)
    inputs = torch.randn(4, 3, 32, 32)

    assert model(inputs).shape == (4, 10)
