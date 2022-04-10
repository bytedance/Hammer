# python3.7
"""Contains the class of paired dataset.

`PairedDataset` is commonly used as the dataset that provides image pairs. This
is widely used for training tasks like pix2pix. Notably, a pair of images may go
through different transformation pipelines as the data augmentation.
"""

import warnings
import numpy as np

from .base_dataset import BaseDataset

__all__ = ['PairedDataset']


class PairedDataset(BaseDataset):
    """Defines the paired dataset class.

    The returned item format looks like::

        {
            'index': int,
            'raw_image_A': np.ndarray,
            'raw_image_B': np.ndarray,
            'image_A': np.ndarray,
            'image_B': np.ndarray
        }

    Available transformation kwargs:

    - Basic settings:
        - image_size: Final image size produced by the dataset if `crop_size` is
            not provided. Otherwise, `crop_size` will be the final size.
            (required)
    - Decode settings:
        - image_channels_A (default: 3)
        - image_channels_B (default: 3)
    - Pre-crop (center crop) settings:
        - pre_crop_size (default: None)
    - Random region brightness settings:
        - rb_prob (default: 0.0)
        - rb_brightness_change (default: 0.6)
        - rb_center_x_range (default: (0.2, 0.8))
        - rb_center_y_range (default: (0.25, 0.75))
        - rb_num_vertices (default: 40)
        - rb_radius_range (default: (0, 0.25))
        - rb_spikyness_range (default: (0.1, 0.1))
        - rb_irregularity_range (default: (0, 1))
        - rb_max_blur_kernel_ratio (default: 0.025)
        - rb_min_blur_kernel_size (default: 3)
        - rb_blur_x_std (default: 3)
        - rb_blur_y_std (default: None)
        - rb_prefetch_queue_depth (default: 32)
    - Random affine settings:
        - ra_prob (default: 0.0)
        - ra_rotation_range (default: (-15, 15))
        - ra_scale_range (default: (0.95, 1.05))
        - ra_tx_range (default: (-0.02, 0.02))
        - ra_ty_range (default: (-0.02, 0.02))
        - ra_prefetch_queue_depth (default: 32)
    - Random crop settings:
        - crop_size (default: image_size)
    - Random flip settings:
        - hflip_prob (default: 0.0)
        - vflip_prob (default: 0.0)
    - Random HSV settings:
        NOTE:
            Parameters are lower and upper bounds for H, S, V jittering range.
            Setting as (0, 0, 1, 1, 1, 1) disables HSV jittering.

        - hsv_param (default: (0, 0, 1, 1, 1, 1))
        - hsv_param_B (default: (0, 0, 1, 1, 1, 1))
        - hsv_aug_B: Whether image B requires HSV augmentation. (default: False)
        - separate_hsv_aug: Whether to apply HSV augmentation to image A/B
            separately. (default: False)
    - Random blur and sharpen settings (to image A only):
        - blur_prob (default: 0.0)
        - sharpen_prob (default: 0.0)
        - rbs_kernel_range (default: (3, 7))
        - rbs_sharpen_range (default: (1.5, 2.0))
    - Random image compression settings (to image A only):
        - rc_prob (default: 0.0)
        - rc_quality_range (default: (40, 60))
    - Random image downsampling augmentation settings (to image A only):
        - rd_prob (default: 0.0)
        - rd_down_range (default: (1, 2.5))
    - Normalization settings:
        - min_val (default: -1.0)
        - max_val (default: 1.0)
    """

    def __init__(self,
                 root_dir,
                 file_format='zip',
                 annotation_path=None,
                 annotation_meta=None,
                 annotation_format='json',
                 max_samples=-1,
                 mirror=False,
                 transform_kwargs=None):
        super().__init__(root_dir=root_dir,
                         file_format=file_format,
                         annotation_path=annotation_path,
                         annotation_meta=annotation_meta,
                         annotation_format=annotation_format,
                         max_samples=max_samples,
                         mirror=mirror,
                         transform_kwargs=transform_kwargs)

    def get_raw_data(self, idx):
        # Handle data mirroring.
        do_mirror = self.mirror and idx >= (self.num_samples // 2)
        if do_mirror:
            idx = idx - self.num_samples // 2

        image_path_A, image_path_B = self.items[idx][:2]

        # Load image to buffer.
        buffer_A = np.frombuffer(self.fetch_file(image_path_A), dtype=np.uint8)
        buffer_B = np.frombuffer(self.fetch_file(image_path_B), dtype=np.uint8)

        idx = np.array(idx)
        do_mirror = np.array(do_mirror)
        return [idx, do_mirror, buffer_A, buffer_B]

    @property
    def num_raw_outputs(self):
        return 4  # [idx, do_mirror, buffer_A, buffer_B]

    def parse_transform_config(self):
        image_size = self.transform_kwargs.get('image_size')

        # Decode.
        image_channels_A = self.transform_kwargs.setdefault(
            'image_channels_A', 3)
        image_channels_B = self.transform_kwargs.setdefault(
            'image_channels_B', 3)
        self.transform_config = dict(
            decode_A=dict(transform_type='Decode',
                          image_channels=image_channels_A,
                          return_square=False,
                          center_crop=False),
            decode_B=dict(transform_type='Decode',
                          image_channels=image_channels_B,
                          return_square=False,
                          center_crop=False)
        )

        # Crop and resize.
        pre_crop_size = self.transform_kwargs.setdefault('pre_crop_size', None)
        self.transform_config.update(
            center_crop=dict(transform_type='CenterCrop',
                             crop_size=pre_crop_size),
            resize=dict(transform_type='Resize', image_size=image_size)
        )
        if pre_crop_size is None:
            self.transform_config.update(
                center_crop=dict(transform_type='Identity')
            )

        # Random region brightness
        rb_prob = self.transform_kwargs.setdefault('rb_prob', 0.0)
        rb_brightness_change = self.transform_kwargs.get(
            'rb_brightness_change', 0.6)
        rb_center_x_range = self.transform_kwargs.get(
            'rb_center_x_range', (0.2, 0.8))
        rb_center_y_range = self.transform_kwargs.get(
            'rb_center_y_range', (0.25, 0.75))
        rb_num_vertices = self.transform_kwargs.get('rb_num_vertices', 40)
        rb_radius_range = self.transform_kwargs.get(
            'rb_radius_range', (0, 0.25))
        rb_spikyness_range = self.transform_kwargs.get(
            'rb_spikyness_range', (0.1, 0.1))
        rb_irregularity_range = self.transform_kwargs.get(
            'rb_irregularity_range', (0, 1))
        rb_max_blur_kernel_ratio = self.transform_kwargs.get(
            'rb_max_blur_kernel_ratio', 0.025)
        rb_min_blur_kernel_size = self.transform_kwargs.get(
            'rb_min_blur_kernel_size', 3)
        rb_blur_x_std = self.transform_kwargs.get('rb_blur_x_std', 3)
        rb_blur_y_std = self.transform_kwargs.get('rb_blur_y_std', None)
        rb_prefetch_queue_depth = self.transform_kwargs.get(
            'rb_prefetch_queue_depth', 32)
        self.transform_config.update(
            random_region_brightness=dict(
                transform_type='RegionBrightness',
                image_size=image_size,
                image_channels=image_channels_A,
                prob=rb_prob,
                brightness_change=rb_brightness_change,
                center_x_range=rb_center_x_range,
                center_y_range=rb_center_y_range,
                num_vertices=rb_num_vertices,
                radius_range=rb_radius_range,
                spikyness_range=rb_spikyness_range,
                irregularity_range=rb_irregularity_range,
                max_blur_kernel_ratio=rb_max_blur_kernel_ratio,
                min_blur_kernel_size=rb_min_blur_kernel_size,
                blur_x_std=rb_blur_x_std,
                blur_y_std=rb_blur_y_std,
                prefetch_queue_depth=rb_prefetch_queue_depth)
        )
        if rb_prob != 0 and image_channels_A != image_channels_B:
            # DALI does not support broadcasting for tensor multiplication,
            # hence the region mask should be pre-repeated to be with the same
            # number of channels as the images (A and B). If images A and B have
            # different number of channels, it will raise an error given the
            # same mask. Please refer to
            # `datasets/transformations/region_brightness.py` and
            # `datasets/utils/polygon.py` for more details.
            warnings.warn('Random region brightness augmentation will be '
                          'ignored since image A and image B have different '
                          'number of channels!')
            rb_prob = 0
            self.transform_kwargs['rb_prob'] = 0
        if rb_prob == 0:
            self.transform_config.update(
                random_region_brightness=dict(transform_type='Identity')
            )

        # Random affine.
        ra_prob = self.transform_kwargs.setdefault('ra_prob', 0.0)
        ra_rotation_range = self.transform_kwargs.get(
            'ra_rotation_range', (-15, 15))
        ra_scale_range = self.transform_kwargs.get(
            'ra_scale_range', (0.95, 1.05))
        ra_tx_range = self.transform_kwargs.get('ra_tx_range', (-0.02, 0.02))
        ra_ty_range = self.transform_kwargs.get('ra_ty_range', (-0.02, 0.02))
        ra_prefetch_queue_depth = self.transform_kwargs.get(
            'ra_prefetch_queue_depth', 32)
        self.transform_config.update(
            random_affine=dict(transform_type='AffineTransform',
                               image_size=image_size,
                               prob=ra_prob,
                               rotation_range=ra_rotation_range,
                               scale_range=ra_scale_range,
                               tx_range=ra_tx_range,
                               ty_range=ra_ty_range,
                               prefetch_queue_depth=ra_prefetch_queue_depth)
        )
        if ra_prob == 0:
            self.transform_config.update(
                random_affine=dict(transform_type='Identity')
            )

        # Random crop.
        crop_size = self.transform_kwargs.setdefault('crop_size', image_size)
        self.transform_config.update(
            random_crop=dict(transform_type='RandomCrop', crop_size=crop_size)
        )
        if crop_size == image_size:
            self.transform_config.update(
                random_crop=dict(transform_type='Identity')
            )

        # Random flip.
        hflip_prob = self.transform_kwargs.setdefault('hflip_prob', 0.0)
        vflip_prob = self.transform_kwargs.setdefault('vflip_prob', 0.0)
        self.transform_config.update(
            random_flip=dict(transform_type='Flip',
                             horizontal_prob=hflip_prob,
                             vertical_prob=vflip_prob)
        )
        if hflip_prob == 0 and vflip_prob == 0:
            self.transform_config.update(
                random_flip=dict(transform_type='Identity')
            )

        # Random HSV.
        hsv_param = self.transform_kwargs.get('hsv_param', (0, 0, 1, 1, 1, 1))
        hsv_param_B = self.transform_kwargs.get(
            'hsv_param_B', (0, 0, 1, 1, 1, 1))
        self.transform_config.update(
            random_hsv=dict(transform_type='HSVJittering',
                            h_range=hsv_param[0:2],
                            s_range=hsv_param[2:4],
                            v_range=hsv_param[4:6]),
            random_hsv_B=dict(transform_type='HSVJittering',
                              h_range=hsv_param_B[0:2],
                              s_range=hsv_param_B[2:4],
                              v_range=hsv_param_B[4:6])
        )
        hsv_aug_B = self.transform_kwargs.setdefault('hsv_aug_B', False)
        separate_hsv_aug = self.transform_kwargs.setdefault(
            'separate_hsv_aug', False)
        if hsv_param == (0, 0, 1, 1, 1, 1):
            self.transform_config.update(
                random_hsv=dict(transform_type='Identity')
            )
        if not hsv_aug_B:
            self.transform_config.update(
                random_hsv_B=dict(transform_type='Identity')
            )
        elif hsv_aug_B and not separate_hsv_aug:
            self.transform_config.pop('random_hsv_B')
        else:
            if hsv_param_B == (0, 0, 1, 1, 1, 1):
                self.transform_config.update(
                    random_hsv_B=dict(transform_type='Identity')
                )

        # Random blur and sharpen.
        blur_prob = self.transform_kwargs.setdefault('blur_prob', 0.0)
        sharpen_prob = self.transform_kwargs.setdefault('sharpen_prob', 0.0)
        rbs_kernel_range = self.transform_kwargs.get('rbs_kernel_range', (3, 7))
        rbs_sharpen_range = self.transform_kwargs.get(
            'rbs_sharpen_range', (1.5, 2.0))
        self.transform_config.update(
            random_blur_sharpen=dict(transform_type='BlurAndSharpen',
                                     blur_prob=blur_prob,
                                     sharpen_prob=sharpen_prob,
                                     kernel_range=rbs_kernel_range,
                                     sharpen_range=rbs_sharpen_range)
        )
        if blur_prob == 0 and sharpen_prob == 0:
            self.transform_config.update(
                random_blur_sharpen=dict(transform_type='Identity')
            )

        # Random compress.
        rc_prob = self.transform_kwargs.setdefault('rc_prob', 0.0)
        rc_quality_range = self.transform_kwargs.get(
            'rc_quality_range', (40, 60))
        self.transform_config.update(
            random_compress=dict(transform_type='JpegCompress',
                                 prob=rc_prob, quality_range=rc_quality_range)
        )
        if rc_prob == 0:
            self.transform_config.update(
                random_compress=dict(transform_type='Identity')
            )

        # Random downsample.
        rd_prob = self.transform_kwargs.setdefault('rd_prob', 0.0)
        rd_down_range = self.transform_kwargs.get('rd_down_range', (1, 2.5))
        self.transform_config.update(
            random_downsample=dict(transform_type='ResizeAug',
                                   image_size=crop_size,
                                   prob=rd_prob, down_range=rd_down_range)
        )
        if rd_prob == 0:
            self.transform_config.update(
                random_downsample=dict(transform_type='Identity')
            )

        # Normalize output.
        min_val = self.transform_kwargs.setdefault('min_val', -1.0)
        max_val = self.transform_kwargs.setdefault('max_val', 1.0)
        self.transform_config.update(
            normalize=dict(transform_type='Normalize',
                           min_val=min_val, max_val=max_val)
        )

    def transform(self, raw_data, use_dali=False):
        idx, do_mirror, buffer_A, buffer_B = raw_data

        raw_image_A = self.transforms['decode_A'](buffer_A, use_dali=use_dali)
        raw_image_B = self.transforms['decode_B'](buffer_B, use_dali=use_dali)
        raw_data = [raw_image_A, raw_image_B]
        raw_data = self.transforms['center_crop'](raw_data, use_dali=use_dali)
        raw_data = self.transforms['resize'](raw_data, use_dali=use_dali)
        raw_data = self.mirror_aug(raw_data, do_mirror, use_dali=use_dali)

        data = self.transforms['random_region_brightness'](
            raw_data, use_dali=use_dali)
        data = self.transforms['random_affine'](data, use_dali=use_dali)
        data = self.transforms['random_crop'](data, use_dali=use_dali)
        data = self.transforms['random_flip'](data, use_dali=use_dali)
        if 'random_hsv_B' in self.transforms:
            image_A = self.transforms['random_hsv'](data[0], use_dali=use_dali)
            image_B = self.transforms['random_hsv_B'](
                data[1], use_dali=use_dali)
        else:
            image_A, image_B = self.transforms['random_hsv'](
                data, use_dali=use_dali)
        image_A = self.transforms['random_blur_sharpen'](
            image_A, use_dali=use_dali)
        image_A = self.transforms['random_compress'](image_A, use_dali=use_dali)
        image_A = self.transforms['random_downsample'](
            image_A, use_dali=use_dali)
        data = self.transforms['normalize'](
            [image_A, image_B], use_dali=use_dali)

        return idx, raw_data[0], raw_data[1], data[0], data[1]

    @property
    def output_keys(self):
        return ['index', 'raw_image_A', 'raw_image_B', 'image_A', 'image_B']
