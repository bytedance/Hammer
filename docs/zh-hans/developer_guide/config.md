# 编写 Config 配置实验

Hammer 使用 [click](https://click.palletsprojects.com/en/8.0.x/) 来从命令行解析参数并运行任务，这一选择主要出于对嵌套解析和子命令的需要。

**在编写 Config 之前，最好先熟悉一下 [click](https://click.palletsprojects.com/en/8.0.x/) 以避免意料之外的行为。**

> 注：一个与 `click.option` 相关的常见问题是，`click` 会 [自动转换你的参数名](https://click.palletsprojects.com/en/8.0.x/options/#name-your-options)：
>
> "-f", "--foo-bar", the name is `foo_bar`
>
> "-x", the name is `x`
>
> "-f", "--filename", "dest", the name is `dest`
>
> "--CamelCase", the name is `camelcase`
>
> "-f", "-fb", the name is `f`
>
> "--f", "--foo-bar", the name is `f`
>
> "---f", the name is `_f`

## 解析过程概览

```{mermaid}

    sequenceDiagram
        participant train as train.py 
        participant base as configs/base_config.py
        participant custom as configs/YOUR_CONFIG.py
        
        Note over train, custom: 将所有 commands 注册以待识别
        loop for every config
            train->>base: `get_command()`
            base->>+custom: `get_options()`
            custom-->>-train: Add to `command_group`
        end
        
        Note over train, custom: 从命令行解析所有的参数
        train->>base: `get_config()`
        base->>+custom: `parse_options()`
        base->>custom: `update_options()`
        custom-->>-train: Give parsed `config` to `runner`.
```

如上图所示，与 config 相关的有两个阶段：
每当启动训练时，`train.py` 将 **1)** 迭代每个配置文件以首先注册所有要识别的命令，然后 **2)** 从命令行解析参数。

具体来说，每个配置文件代表一个任务的一组设置，用于训练或微调模型，以及程序如何解析这些设置。
每个任务都是 `click` 实例的 `command`，每个设置都是从命令行解析参数（通常以`--`开头）的 `option`。

> 例如，`stylegan2` 是 `train.py` 的命令，用于启动 StyleGAN2 训练任务，而 `--train_dataset` 是指定此任务的训练数据集的选项。

### 阶段 1: 将所有 commands 注册以待识别

从每个配置文件中，`train.py` 将调用 `get_command()`（在 `BaseConfig` 中），它进一步调用 `get_options()`（在派生的配置类中）以获取此配置的 options。
仅当 `train.py` 已将此类的 command 和 options 注册到 `command_group` 中时，才能从命令行解析 command 和 options。
上面的过程几乎是由基类完成的，而且是在实际解析之前完成的。

### 阶段 2: 从命令行解析所有的参数

遍历所有配置文件后，所有 command 和 options 才能被识别。
`train.py` 将根据给定的 command 在目标配置中调用 `get_config()`。
在 `get_config()` 中，它首先调用 `parse_options()` 将命令行参数转换为 Python 对象，然后在需要时调用 `update_config()` 来修改配置（除了选项，*例如*，metric 的配置）。

## 编写你自己的 Config 文件

**如果你只是想改变一些超参数（*例如*，增加`batch_size`），你不需要编写新的 config 文件，只需从命令行传入新的设置就足够了。**
但是，如果你打算修改任务流程（*例如*，添加新的 loss 项或引入更多模型），你可能需要编写自己的 config 文件。

要新建一个 config 文件，请将其放在 `configs/` 目录下，并从 `configs/base_config.py` 继承 `BaseConfig` 类，该类包含所有任务的一些基本的设置。
然后，你需要做的就是在方法 `get_options()` 中编写所有可能的设置（除了 `BaseConfig` 中的设置），并在方法 `parse_options()` 中编写解析它们的方法。
你可以转到任何已写入的配置文件以供参考。

### 例子

这里我们以编写 StyleGAN2 的 config 为例：

1. 新建文件`configs/stylegan2_config.py`。
2. 在`configs/stylegan2_config.py`中，定义继承自`BaseConfig`的类`StyleGAN2Config`。
   然后，在 `configs/__init__.py` 中，导入 `StyleGAN2Config` 并放入 `CONFIG_POOL`。
3. 重要的设置（如 runner、dataset、model 和要使用的 loss）应该放在配置文件的顶部并大写。
4. 在 `class StyleGAN2Config(BaseConfig):` 之后是一些静态属性：
   * `name` 是 command 名称，换句话说，**这个词对于在命令行界面中触发此配置的关键字**。
   * 如果你运行 `python train.py --help`，`hint` 将用于显示简略的说明信息。
   * 如果你运行 `python train.py stylegan2 --help`，`info` 将用于显示此时更详细的说明消息。
5. 在 `get_options()` 中，记得首先使用 `super().get_options()`，然后再扩展你想要在命令行中处理的任何 options。
   * 在 `cls.command_option()` 中，`type` 有助于将参数从命令行转换为 Python 对象。你可以参考 `utils/parsing_utils` 了解更多详细信息。
6. 在`parse_options()`中，请使用 `self.args.pop()` 获取值。
   * 此时你得到的值可能与命令行中的不同，因为它已经按照你上面指定的 `type` 交由 click 进行了处理。
7. 然后，同样在 `parse_options()` 中，写下准备关键字参数以初始化实例的任何后处理和逻辑。
   * 在 `self.config.models.update()` 中，使用了 2 个模型：`discriminator` 和 `generator`。
     `model` 定义了如何初始化这样一个模型，`lr` 定义了如何调整学习率，`opt` 定义了如何初始化优化器，
     `kwargs_train` 定义了在训练期间传入模型的 `forward()` 的关键字参数，而 `kwargs_val` 定义了在验证期间传入模型的 `forward()` 的关键字参数。
   * 在 `self.config.loss.update()` 中，`loss_type` 将识别你选择的 loss，你可以在其余部分写下任何关键字参数。
   * 在 `self.config.controllers.update()` 中，你可以写下任何设置来初始化任务中使用的 controller。确保名称应与目标 controller 的类名匹配。
     对于可用的 controller，请访问`runners/controllers`。
   * 在 `self.config.metrics.update()` 中，你可以写下任何设置来初始化 metric。请注意，我们也将 GAN 可视化结果视为一种 metric。
     确保名称应与目标 metric 的类名匹配。有关可用 metric，请访问 `metrics/`。