# An Efficient Library for Training Deep Models

This repository provides an efficient PyTorch-based library for training deep models.

## Installation

Make sure your Python >= 3.7, CUDA version >= 11.1, and CUDNN version >= 7.6.5.

1. Install package requirements via `conda`:

    ```shell
    conda create -n <ENV_NAME> python=3.7  # create virtual environment with Python 3.7
    conda activate <ENV_NAME>
    pip install -r requirements/minimal.txt -f https://download.pytorch.org/whl/cu111/torch_stable.html
    ```

2. To use video visualizer (optional), please also install `ffmpeg`.

    - Ubuntu: `sudo apt-get install ffmpeg`.
    - MacOS: `brew install ffmpeg`.

3. To reduce memory footprint (optional), you can switch to either `jemalloc` (recommended) or `tcmalloc` rather than your default memory allocator.

    - jemalloc (recommended):
        - Ubuntu: `sudo apt-get install libjemalloc`
    - tcmalloc:
        - Ubuntu: `sudo apt-get install google-perftools`

4. (optional) To speed up data loading on NVIDIA GPUs, you can install [DALI](https://github.com/NVIDIA/DALI), together with [dill](https://pypi.org/project/dill/) to pickle python objects. It is optional to also install [CuPy](https://cupy.dev/) for some customized operations if needed:

    ```shell
    pip install --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-<CUDA_VERSION>
    pip install dill
    pip install cupy  # optional, installation can be slow
    ```

    For example, on CUDA 11.1, DALI can be installed via:

    ```shell
    pip install --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda110  # CUDA 11.1 compatible
    pip install dill
    pip install cupy  # optional, installation can be slow
    ```

## Quick Demo

### Train StyleGAN2 on FFHQ in Resolution of 256x256

In your Terminal, run:

```shell
./scripts/training_demos/stylegan2_ffhq256.sh <NUM_GPUS> <PATH_TO_DATA> [OPTIONS]
```

where

- `<NUM_GPUS>` refers to the number of GPUs. Setting `<NUM_GPUS>` as 1 helps launch a training job on single-GPU platforms.

- `<PATH_TO_DATA>` refers to the path of FFHQ dataset (in resolution of 256x256) with `zip` format. If running on local machines, a soft link of the data will be created under the `data` folder of the working directory to save disk space.

- `[OPTIONS]` refers to any additional option to pass. Detailed instructions on available options can be shown via `./scripts/training_demos/stylegan2_ffhq256.sh <NUM_GPUS> <PATH_TO_DATA> --help`.

This demo script uses `stylegan2_ffhq256` as the default value of `job_name`, which is particularly used to identify experiments. Concretely, a directory with name `job_name` will be created under the root working directory (with is set as `work_dirs/` by default). To prevent overwriting previous experiments, an exception will be raised to interrupt the training if the `job_name` directory has already existed. To change the job name, please use `--job_name=<NEW_JOB_NAME>` option.

### More Demos

Please find more training demos under `./scripts/training_demos/`.

## Inspect Training Results

Besides using TensorBoard to track the training process, the raw results (e.g., training losses and running time) are saved in JSON format. They can be easily inspected with the following script

```python
import json

file_name = '<PATH_TO_WORK_DIR>/log.json'

data_entries = []
with open(file_name, 'r') as f:
    for line in f:
        data_entry = json.loads(line)
        data_entries.append(data_entry)

# An example of data entry
# {"Loss/D Fake": 0.4833524551040682, "Loss/D Real": 0.4966000154727226, "Loss/G": 1.1439273656869773, "Learning Rate/Discriminator": 0.002352941082790494, "Learning Rate/Generator": 0.0020000000949949026, "data time": 0.0036810599267482758, "iter time": 0.24490128830075264, "run time": 66108.140625}
```

## Convert Pre-trained Models

See [Model Conversion](./docs/model_conversion.md) for details.

## Prepare Datasets

See [Dataset Preparation](./docs/dataset_preparation.md) for details.

## Develop

See [Contributing Guide](./CONTRIBUTING.md) for details.

## License

The project is under [MIT License](./LICENSE).

## Acknowledgement

This repository originates from [GenForce](https://github.com/genforce/genforce), with all modules carefully optimized to make it more flexible and robust for distributed training. On top of [GenForce](https://github.com/genforce/genforce) where only [StyleGAN](https://github.com/NVlabs/stylegan) training is provided, this repository also supports training [StyleGAN2](https://github.com/NVlabs/stylegan2) and [StyleGAN3](https://github.com/NVlabs/stylegan3), both of which are fully reproduced. *Any new method is welcome to merge into this repository! Please refer to the **Develop** section.*

### Contributors

The main contributors are listed as follows.

| Member                                       | Contribution |
| :--                                          | :-- |
|[Yujun Shen](https://shenyujun.github.io/)    | Refactor and optimize the entire codebase and reproduce state-of-the-art approaches.
|[Zhiyi Zhang](https://github.com/BrandoZhang) | Contribute to a number of sub-modules and functions, especially dataset related.
|[Dingdong Yang](https://github.com/santisy)   | Contribute to DALI data loading acceleration.
|[Yinghao Xu](https://justimyhxu.github.io/)   | Originally contribute to runner and loss functions in [GenForce](https://github.com/genforce/genforce).
|[Ceyuan Yang](https://ceyuan.me/)             | Originally contribute to data loader in [GenForce](https://github.com/genforce/genforce).
|[Jiapeng Zhu](https://zhujiapeng.github.io/)  | Originally contribute to evaluation metrics in [GenForce](https://github.com/genforce/genforce).

## BibTex

We open source this library to the community to facilitate the research. If you do like our work and use the codebase for your projects, please cite our work as follows.

```bibtex
@misc{hammer2022,
  title =        {Hammer: An Efficient Toolkit for Training Deep Models},
  author =       {Shen, Yujun and Zhang, Zhiyi and Yang, Dingdong and Xu, Yinghao and Yang, Ceyuan and Zhu, Jiapeng},
  howpublished = {\url{https://github.com/bytedance/Hammer}},
  year =         {2022}
}
```
