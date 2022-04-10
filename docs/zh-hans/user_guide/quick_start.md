# 快速上手

## 以在 CIFAR-10 上训练 StyleGAN2-ADA 为例

### 配置环境
请先参阅项目 README 配置运行环境。

### 准备数据集

创建两个文件夹，一个用于保存下载到的原始数据 (`raw_data`)，一个用于存放处理好的数据 (`data`)。

> 对于 CIFAR-10 数据集，这里的处理只是将类别标签转换为 Hammer 支持的格式，并将文件从 `.tar.gz` 转为 `.zip`。

```shell
mkdir -p ../raw_data
mkdir -p ../data
```

在 Hammer 主路径执行以下命令，会自动拉取 CIFAR-10 的训练数据到 `../raw_data` 并将处理好的数据保存为 `../data/cifar10.zip`。

```shell
python prepare_dataset.py ../raw_data ../data/cifar10.zip --dataset cifar10 --portion train
```

### 修改配置

可在样例脚本 `./scripts/training_demos/stylegan2ada_cifar10.sh` 了解到 [原作](https://github.com/NVlabs/stylegan2-ada-pytorch) 的默认配置。

有任何想修改的配置可以直接在脚本中修改，或是在执行脚本时通过 `--<SETTING>=<NEW_VALUE>` 的形式覆盖。

### 发起实验

```shell
./scripts/training_demos/stylegan2ada_cifar10.sh <NUM_GPUS> <ABS_PATH_TO_cifar10.zip> [OPTIONS]
```

其中：

- `<NUM_GPUS>` 需要改成所用 GPU 的个数，哪怕 `<NUM_GPUS>` 替换为 1 也可以运行单卡训练；

- `<ABS_PATH_TO_cifar10.zip>` 替换为数据集的 **绝对路径** （直接指向一个 `.zip`），如果是一个本地已存在的路径，会在 `work_dirs/stylegan2ada_cifar10/data` 创建对其的软链接，节约空间；

- `[OPTIONS]` 为可选，接受任何能应用在 StyleGAN2 上的设置，如传入 `--help` 会打印所有可用 options 的含义。 

### 观察训练过程

#### 终端输出

在训练过程的信息统计中：
  - Iter （包括旁边括号里的图片数）：当前的训练进度；
  - loss_xxx：用户定义的 loss；
  - Gs_beta：G exponential moving average 的参数；
  - lr (xxx)：对应 model 的 learning rate；
  - aug_prob：Adaptive augmentation 当前的概率；
  - data time：除了 forward/backward 以外的时间都在这，包括但不限于 数据的读取耗时、controller 耗时等；
  - iter time：连续两次 log 期间 iterations 的平均耗时；
  - run time：已运行时间；
  - GPU memory：连续两次 log 期间主进程占用过的最大显存，不是 log 时的实时显存占用；
  - Rank00 memory：log 时的主进程内存占用；
  - Total memory：log 时的所有进程内存占用，需注意目前的实现暂未统计到 dataloader 进程，因此实际总内存开销会比这个值略高一些；
  - Disk free：运行路径所在磁盘的剩余空间；
  - ETA：预计剩余时间，由于第一个 Iter 的 log 算上了初始化的时间，所以后面几轮里的 ETA 才比较准确。

#### 工作路径结构

```shell
work_dirs/
└── stylegan2ada_cifar10/                               # 根据 `--job_name` 创建的目录，需保证唯一
    ├── checkpoints/                                    # 存储了训练产生的节点
    │   ├── best-fid50k_full-checkpoint-000001.pth      #   最佳节点会以 `best-xxx` 形式命名
    │   └── checkpoint-000001.pth                       #   普通的中间过程节点
    ├── config.json                                     # JSON 格式的 config，方便按语义解析和复盘
    ├── data/                                           # 存储了训练所需数据：数据集、预训练模型等
    │   └── cifar10.zip -> <ABS_PATH_TO_cifar10.zip>    #   数据集软链接，方便复盘
    ├── events/                                         # TensorBoard 文件，可以在终端运行 tensorboard --host 0.0.0.0 --logdir <PATH_TO_EVENTS> 来启动 TensorBoard
    ├── log.jsonl                                       # JSONL 格式的 Log，方便按语义解析，本质上与 `log.txt` 内容一致
    ├── log.txt                                         # 适于人类阅读的 Log 文件
    ├── resources/                                      # 与系统资源相关的 Log
    │   ├── all_proc_info.jsonl                         #   所有进程的资源信息
    │   └── rank00_proc_info.jsonl                      #   主进程的资源信息
    └── results/                                        # 存储了与训练结果相关的内容
        ├── fid50k_full_labels_50000.npy                #   计算 FID50K_Full 时的 label 缓存，保证每次 val 时所用的 label 一致
        ├── fid50k_full_latents_50000.npy               #   计算 FID50K_Full 时的 latent 缓存，保证每次 val 时所用的 latent 一致
        ├── fid50k_full.txt                             #   历次计算 FID50K_Full 的结果
        ├── real_data-000001.png                        #   训练数据的样例
        ├── snapshot-000001.png                         #   Iter-000001 的生成样例
        ├── snapshot_labels_32.npy                      #   可视化生成图片时的 label 缓存，保证训练过程中每次生成图片时所用的 label 一致
        └── snapshot_latents_32.npy                     #   可视化生成图片时的 latent 缓存，保证训练过程中每次生成图片时所用的 latent 一致

5 directories, 15 files
```
