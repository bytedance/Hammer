# 模型转换

## 引言

除了训练，我们还支持从官方发布的模型中转换预训练的模型权重，并使用它们进行推理。 
因此，如果你已经使用官方开源代码库训练了一些模型，请不要担心，我们已经确保它们与我们的代码库完全匹配！ 
我们现在支持使用以下存储库训练的模型：

- [PGGAN](https://github.com/tkarras/progressive_growing_of_gans) (TensorFlow)
- [StyleGAN](https://github.com/NVlabs/stylegan) (TensorFlow)
- [StyleGAN2](https://github.com/NVlabs/stylegan2) (TensorFlow)
- [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada) (TensorFlow)
- [StyleGAN2-ADA-PyTorch](https://github.com/NVlabs/stylegan2-ada-pytorch) (PyTorch)
- [StyleGAN3](https://github.com/NVlabs/stylegan3) (PyTorch)

**注：** 我们的代码库完全建立在 PyTorch 之上。 
因此，如果要转换官方的 TensorFlow 模型，则需要配置 TensorFlow 环境。 
如果只需要模型转换而无需测试，CPU 版本的 TensorFlow 就足够了。 
如果你还想测试转换精度，则需要 GPU 版本的 TensorFlow 来运行源模型。 
我们建议建立一个独立的模型转换环境，通过以下命令：

```shell
conda create -n <TF_ENV_NAME> python=3.7  # create virtual environment with Python 3.7
conda activate <TF_ENV_NAME>
conda install cudatoolkit=10.0 cudnn=7.6.5
pip install -r requirements/convert.txt
```

## 用法

我们为模型转换提供了一个脚本`convert_model.py`。 例如，要转换一个预训练的 [StyleGAN2](https://github.com/NVlabs/stylegan2) 模型（官方的 TensorFlow 版本），只需运行：

```shell
python convert_model.py stylegan2 \
       --source_model_path ${SOURCE_MODEL_PATH} \
       --target_model_path ${TARGET_MODEL_PATH} \
       --forward_test_num 10 \
       --backward_test_num 0 \
       --save_test_image
```

上述命令将执行模型转换，然后检查转换精度（前向传播 10 次对比误差，没有测试反向传播）。

谨记这个环境仅用于模型转换。 之后，请通过以下方式切换回原来的环境：

```shell
conda deactivate
conda activate <ENV_NAME>
```

## Submodules

要转换模型，应首先下载源代码。 
我们已将原始仓库添加为本仓库的子模块，可以通过运行 `git submodule update --init <submodule_name>` 对其进行初始化。 
在这里，`<submodule_name>` 可以是以下任何一种：

- `converters/pggan_official`: [PGGAN](https://github.com/tkarras/progressive_growing_of_gans)
- `converters/stylegan_official`: [StyleGAN](https://github.com/NVlabs/stylegan)
- `converters/stylegan2_official`: [StyleGAN2](https://github.com/NVlabs/stylegan2)
- `converters/stylegan2ada_tf_official`: [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada)
- `converters/stylegan2ada_pth_official`: [StyleGAN2-ADA-PyTorch](https://github.com/NVlabs/stylegan2-ada-pytorch)
- `converters/stylegan3_official`: [StyleGAN3](https://github.com/NVlabs/stylegan3)

或者，你可以用 `git submodule update --init --recursive` 一步下载所有源码。

由于这些代码将 **仅用于模型转换**，且之后不会再被使用。因此，可以通过运行 `git submodule deinit <submodule_name> -f` 安全地删除 submodules，其中 `-f` 选项将强制删除已编译的文件，例如 `__pycache__`。