# Experiments

The default smoke run uses generated 32×32 RGB images. Its accuracy is not
scientifically meaningful; it validates data loading, training, evaluation, and
result writing.

To use CIFAR-10, duplicate the configuration, set `dataset = "cifar10"`, remove
batch limits, and increase the number of epochs.
