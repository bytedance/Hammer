# Write a Job Config

Hammer relies on [click](https://click.palletsprojects.com/en/8.0.x/) to parse arguments from command line to launch a job. 
This choice is mainly due to the need of nested parsing and subcommands. 

**Before writing a job config, please get a glance of [click](https://click.palletsprojects.com/en/8.0.x/) to avoid unexpected behaviors.**

> Note: a common issue when writing `click.option` is, `click` will [convert your argument name](https://click.palletsprojects.com/en/8.0.x/options/#name-your-options):
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

## Overview of Parsing Process

```{mermaid}

    sequenceDiagram
        participant train as train.py 
        participant base as configs/base_config.py
        participant custom as configs/YOUR_CONFIG.py
        
        Note over train, custom: Register all commands to be recognized.
        loop for every config
            train->>base: `get_command()`
            base->>+custom: `get_options()`
            custom-->>-train: Add to `command_group`
        end
        
        Note over train, custom: Parse all arguments from command line.
        train->>base: `get_config()`
        base->>+custom: `parse_options()`
        base->>custom: `update_options()`
        custom-->>-train: Give parsed `config` to `runner`.
```

As shown in the figure above, there are two phases related to config.
Whenever launching a training, `train.py` will **1)** iterate every config file to register all commands to be recognized first, and then **2)** parse the arguments from command line.

Concretely, each config file represents a bunch of settings to a task, either for training or fine-tuning a model, and the way how these settings will be parsed by the program. 
Each task is a `command` of the `click` instance, and each setting is an `option` that parses an argument (commonly starts with `--`) from command line.
> For example, `stylegan2` is a command of `train.py` to launch a StyleGAN2 training task, and `--train_dataset` is an option to specify the training dataset for this task. 

### Phase-1: Register commands to be recognized

From each config file, `train.py` will invoke `get_command()` (in `BaseConfig`), which further calls `get_options()` (in the derived config class) to acquire options for this config.
Commands and options can be parsed from command line only if `train.py` has registered such a command and options into `command_group`.
The above process is almost done by base classes, and it is done before the actual parsing.

### Phase-2: Parse arguments from command line

After iterating all config files, all commands and options are ready to be recognized.
`train.py` will call `get_config()` in the target config according to given command.
In `get_config()`, it first invokes `parse_options()` to translate command line arguments to Python object, and then calls `update_config()` to modify configurations (besides options, *e.g.*, metric configs) if needed. 

## Write Your Own Config File

**If you just want to change some hyper-parameters (*e.g.*, increasing the `batch_size`), you don't need to write a new config file, simply parsing the new setting from command line is enough.**
However, if you intend to modify the task pipeline (*e.g.*, adding new loss term or involving more models), you probably need to write your own config.

To new a config file, please put it under the directory of `configs/` and inherit the `BaseConfig` class from `configs/base_config.py`, which contains some basic and handy settings for all tasks.
Then, all you need to do is, writing all possible settings (except those in `BaseConfig`) in method `get_options()`, and writing the way to parse them in method `parse_options()`.
You can turn to any writen config files for reference.

### Example

Here, we take writing StyleGAN2 config as an example.

1. New file `configs/stylegan2_config.py`.
2. In `configs/stylegan2_config.py`, define class `StyleGAN2Config` which inherited from `BaseConfig`. 
   Then, in `configs/__init__.py`, import `StyleGAN2Config` and put it into `CONFIG_POOL`.
3. The most important settings (*i.e.*, the runner, dataset, models, and loss to be used) should be put in the top of config files and in UPPER CASE.
4. Right after `class StyleGAN2Config(BaseConfig):` are static properties.
   * `name` is the command name, *i.e.*, the keyword to trigger this config in command line interface.
   * `hint` will be used to display help message if you run `python train.py --help`.
   * `info` will be used to display help message if you run `python train.py stylegan2 --help`.
5. In `get_options()`, remember to `super().get_options()` first, and then extend any options you would like to handle in command line.
   * In `cls.command_option()`, the `type` helps convert an argument from command line into Python object. You can refer to `utils/parsing_utils` for more details.
6. In `parse_options()`, please use `self.args.pop()` to get the value.
   * At this time, the value you get may differ from that in command line, since it is already be processed by click according to the `type` you specify above.
7. Then, also in `parse_options()`, write down any post-processing and logic of preparing keyword arguments to initialize instances.
   * In `self.config.models.update()`, there are 2 models in use: `discriminator` and `generator`. 
     The `model` defines how to initialize such a model, `lr` defines how to adjust the learning rate, `opt` defines how to initialize optimizer, 
     `kwargs_train` defines the keyword arguments to pass in the `forward()` of model during training, and `kwargs_val` defines the keyword arguments to pass in the `forward()` of model during validation.
   * In `self.config.loss.update()`, `loss_type` will identify the loss you choose, and you can write down any keyword arguments to be used in the remaining.
   * In `self.config.controllers.update()`, you can write down any settings to initialize controllers used in your task. Make sure the name should match the class name of target controller. 
     For available controllers, please visit `runners/controllers`.
   * In `self.config.metrics.update()`, you can write down any settings to initialize metrics. Please note that we treat GAN visualization result as a kind of metrics as well.
     Make sure the name should match the class name of target metric. For available metrics, please visit `metrics/`.