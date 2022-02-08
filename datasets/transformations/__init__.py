# python3.7
"""Collects all transformations for data pre-processing."""

from .affine_transform import AffineTransform
from .blur_and_sharpen import BlurAndSharpen
from .crop import CenterCrop
from .crop import RandomCrop
from .crop import LongSideCrop
from .decode import Decode
from .flip import Flip
from .hsv_jittering import HSVJittering
from .identity import Identity
from .jpeg_compress import JpegCompress
from .normalize import Normalize
from .region_brightness import RegionBrightness
from .resize import Resize
from .resize import ProgressiveResize
from .resize import ResizeAug

__all__ = ['build_transformation']


_TRANSFORMATIONS = {
    'AffineTransform': AffineTransform,
    'BlurAndSharpen': BlurAndSharpen,
    'CenterCrop': CenterCrop,
    'RandomCrop': RandomCrop,
    'LongSideCrop': LongSideCrop,
    'Decode': Decode,
    'Flip': Flip,
    'HSVJittering': HSVJittering,
    'Identity': Identity,
    'JpegCompress': JpegCompress,
    'Normalize': Normalize,
    'RegionBrightness': RegionBrightness,
    'Resize': Resize,
    'ProgressiveResize': ProgressiveResize,
    'ResizeAug': ResizeAug
}


def build_transformation(transform_type, **kwargs):
    """Builds a transformation based on its class type.

    Args:
        transform_type: Class type to which the transformation belongs,
            which is case sensitive.
        **kwargs: Additional arguments to build the transformation.

    Raises:
        ValueError: If the `transform_type` is not supported.
    """
    if transform_type not in _TRANSFORMATIONS:
        raise ValueError(f'Invalid transformation type: '
                         f'`{transform_type}`!\n'
                         f'Types allowed: {list(_TRANSFORMATIONS)}.')
    return _TRANSFORMATIONS[transform_type](**kwargs)
