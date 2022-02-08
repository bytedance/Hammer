# python3.7
"""Collects all datasets."""

from .image_dataset import ImageDataset
from .paired_dataset import PairedDataset
from .data_loaders import build_data_loader

__all__ = ['build_dataset']

_DATASETS = {
    'ImageDataset': ImageDataset,
    'PairedDataset': PairedDataset
}


def build_dataset(for_training, batch_size, dataset_kwargs, data_loader_kwargs):
    """Builds a dataset with a data loader.

    NOTE: Some arguments for data loader, i.e., within `data_loader_kwargs`,
    will be overwritten by this function, depending on whether the data loader
    is for training and validation. More concretely, these arguments include:

    - `repeat`: If `for_training` is set as `False`, this field will always be
        overwritten as `1` to make sure all validation samples will be used only
        once.
    - `shuffle`: If `for_training` is set as `True`, this field will always be
        overwritten as `True` to prevent the model from memorizing the sequence
        order. Otherwise, this field will always be overwritten as `False` to
        preserve the sequence order for evaluation.
    - `drop_last_batch`: If `for_training` is set as `True`, this field will
        always be overwritten as `True` to make sure all batches have the same
        number of samples. This may also be helpful to avoid the error of using
        `batch_size = 1` for `nn.BatchNorm2d` because it is uncontrollable about
        how many samples the last incomplete batch has. Otherwise, this field
        will always be overwritten as `False` to make sure all samples within
        the validation set are used.
    - `drop_last_sample`: This field will always be overwritten as `False` no
        matter the data loader is for training or validation. It ensures that
        all samples are kept when distributing dataset across replicas. Samples
        are dropped only when producing batches. Please refer to the description
        on `drop_last_batch`.

    Args:
        for_training: Whether the dataset is used for training or not.
        batch_size: Bach size of the built data loader.
        dataset_kwargs: A dictionary, containing the arguments for building
            dataset.
        data_loader_kwargs: A dictionary, containing the arguments for building
            data loader.

    Returns:
        A built data loader based on the target dataset.

    Raises:
        ValueError: If the input `batch_size` is invalid.
        ValueError: If `dataset_kwargs` is not provided, or it does not have the
            key `dataset_type`, or the provided `dataset_type` is not supported.
        ValueError: If `data_loader_kwargs` is not provided, or it does not have
            the key `data_loader_type`.
    """
    for_training = bool(for_training)

    batch_size = int(batch_size)
    if batch_size <= 0:
        raise ValueError(f'Batch size should be a positive integer, '
                         f'but `{batch_size}` is received!')

    if not isinstance(dataset_kwargs, dict):
        raise ValueError(f'`dataset_kwargs` should be a dictionary, '
                         f'but `{type(dataset_kwargs)}` is received!')
    if 'dataset_type' not in dataset_kwargs:
        raise ValueError('`dataset_type` is not found in `dataset_kwargs`!')
    dataset_type = dataset_kwargs.pop('dataset_type')
    if dataset_type not in _DATASETS:
        raise ValueError(f'Invalid dataset type: `{dataset_type}`!\n'
                         f'Types allowed: {list(_DATASETS)}.')

    if not isinstance(data_loader_kwargs, dict):
        raise ValueError(f'`data_loader_kwargs` should be a dictionary, '
                         f'but `{type(data_loader_kwargs)}` is received!')
    if 'data_loader_type' not in data_loader_kwargs:
        raise ValueError('`data_loader_type` is not found in '
                         '`data_loader_kwargs`!')
    data_loader_type = data_loader_kwargs.pop('data_loader_type')

    # Build dataset.
    dataset = _DATASETS[dataset_type](**dataset_kwargs)

    # Build data loader based on the dataset.
    data_loader_kwargs['drop_last_sample'] = False  # Always keep all samples.
    if for_training:
        data_loader_kwargs['shuffle'] = True
        data_loader_kwargs['drop_last_batch'] = True
    else:
        data_loader_kwargs['repeat'] = 1
        data_loader_kwargs['shuffle'] = False
        data_loader_kwargs['drop_last_batch'] = False

    return build_data_loader(data_loader_type=data_loader_type,
                             dataset=dataset,
                             batch_size=batch_size,
                             **data_loader_kwargs)
