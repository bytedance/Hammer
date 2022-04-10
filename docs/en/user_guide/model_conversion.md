# Model Conversion

## Introduction

Besides training, we also support converting pre-trained model weights from officially released models and using them for inference. So, if you have already trained some models with the officially open-sourced codebases, don't worry, we have already made sure that they well match our codebase! We now support models trained with following repositories:

- [PGGAN](https://github.com/tkarras/progressive_growing_of_gans) (TensorFlow)
- [StyleGAN](https://github.com/NVlabs/stylegan) (TensorFlow)
- [StyleGAN2](https://github.com/NVlabs/stylegan2) (TensorFlow)
- [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada) (TensorFlow)
- [StyleGAN2-ADA-PyTorch](https://github.com/NVlabs/stylegan2-ada-pytorch) (PyTorch)
- [StyleGAN3](https://github.com/NVlabs/stylegan3) (PyTorch)

**NOTE:** Our codebase is completely built on PyTorch. However, if you want to convert the official TensorFlow model, you need to set up the TensorFlow environment. If only model conversion is needed (without testing), the CPU version TensorFlow is enough. If you would also like to test the conversion precision, then GPU version TensorFlow is required to run the source model. We recommend to set up an independent environment for model conversion via

```shell
conda create -n <TF_ENV_NAME> python=3.7  # create virtual environment with Python 3.7
conda activate <TF_ENV_NAME>
conda install cudatoolkit=10.0 cudnn=7.6.5
pip install -r requirements/convert.txt
```

## Usage

We provide a script `convert_model.py` for model conversion. For example, to convert a pre-trained [StyleGAN2](https://github.com/NVlabs/stylegan2) model (officially TensorFlow version), just run

```shell
python convert_model.py stylegan2 \
       --source_model_path ${SOURCE_MODEL_PATH} \
       --target_model_path ${TARGET_MODEL_PATH} \
       --forward_test_num 10 \
       --backward_test_num 0 \
       --save_test_image
```

The above command will execute the conversion and then check the conversion precision with 10 forward tests and no backward test.

Recall that, this environment is only used for model conversion. After that, please switch back to the original environment via

```shell
conda deactivate
conda activate <ENV_NAME>
```

## Submodules

To convert a model, the source code should be downloaded first. We add the original repositories as submodules of this repository, which can be initialized via running `git submodule update --init <submodule_name>`. Here, `<submodule_name>` can be any one of the following

- `converters/pggan_official`: [PGGAN](https://github.com/tkarras/progressive_growing_of_gans)
- `converters/stylegan_official`: [StyleGAN](https://github.com/NVlabs/stylegan)
- `converters/stylegan2_official`: [StyleGAN2](https://github.com/NVlabs/stylegan2)
- `converters/stylegan2ada_tf_official`: [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada)
- `converters/stylegan2ada_pth_official`: [StyleGAN2-ADA-PyTorch](https://github.com/NVlabs/stylegan2-ada-pytorch)
- `converters/stylegan3_official`: [StyleGAN3](https://github.com/NVlabs/stylegan3)

Or, you can download them all in one step: `git submodule update --init --recursive`.

Recall that these codes will ONLY be used for model conversion. After that, all codes will not be used anymore. Consequently, a submodule can be safely removed via running `git submodule deinit <submodule_name> -f`, where `-f` option will forcibly remove complied files like `__pycache__`.
