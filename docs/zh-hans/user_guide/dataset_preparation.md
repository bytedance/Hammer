# 准备数据集

我们提供了 `prepare_dataset.py` 作为准备数据集的工具。出于性能的考虑，`zip` 格式的数据集是首选。具体而言，该脚本将收集数据集中的所有图像并将它们保存到 zip 文件中。 此外，该脚本还可以保存数据集的元数据（例如，原始文件名）并生成一个简单的标注文件，该文件将每个图像与一个标签配对。

**注：原始图片会不经任何预处理保留在数据集中。**

## 数据集的格式

通常而言，由 `prepare_dataset.py` 打包的数据集有以下格式：

```shell
Archive:  data.zip

  Length      Date    Time    Name
---------  ---------- -----   ----
   295324  2021-12-09 10:13   0/img0.png
   274588  2021-12-09 10:13   0/img1.png
   295324  2021-12-09 10:13   0/img2.png
   311457  2021-12-09 10:13   0/img3.png
   296092  2021-12-09 10:13   0/img4.png
      ...
   296092  2021-12-09 10:43   99/img229067.png
   295324  2021-12-09 10:43   99/img229068.png
  6302822  2021-12-09 10:43   annotation.json  (标注文件)
---------                     -------
67698819325                     229070 files
```

标注文件的格式形如：

```shell
[["0/img0.png", 0], ["0/img1.png", 0], ..., ["99/img229068.png", 99]]
```

## 用法

### 从 StyleGAN2-ADA 创建的数据集转换

如果你已经使用 [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada-pytorch) 仓库中的 `dataset_tool.py` 准备了一个数据集，那么转换它会非常容易。 
基本上，两个仓库都使用 zip 格式的数据集。 因此，我们只需转换注释文件。 
有关详细信息，请参阅 `prepare_dataset.py`。

可以通过以下命令实现转换：

```shell
python prepare_dataset.py /stylegan2ada/data.zip _unused --dataset 'stylegan2ada'
```

**注意：脚本会将新的注释文件添加到现有数据集中，而不是创建新的。**

### 从头开始创建数据集

通常，可以使用以下命令创建数据集：

```shell
python prepare_dataset.py \
    ${PATH_TO_RAW_DATA} \
    ${SAVE_PATH} \
    --dataset ${DATASET_NAME} \
    --portion ${PORTION}
```

其中：

- `${PATH_TO_RAW_DATA}` 是输入数据集的路径。 对于可自动下载的数据集，它可以指向一个空文件夹。
- `${SAVE_PATH}` 是 `zip` 格式的输出数据集的路径。
- `${DATASET_NAME}` 是 `cifar10`、`cifar100`、`mnist`、`imagenet1k`、`lsun`、`inaturalist` 或 `folder` （用于从自定义文件夹中创建数据集）之一。
- `${PORTION}` 是数据集部分。 例如，对于 `imagenet1k`，可用部分是 “train”、“test” 和 “val”。

## 公共数据集描述

在这里，我们提供了一些公共数据集的基本描述。

### MNIST

[MNIST](http://yann.lecun.com/exdb/mnist/) 包含了 60,000 张图片，其中 50,000 张属于 `train` 部分，另外 10,000 张属于 `test` 部分。请使用以下命令准备 MNIST 数据集：

```shell
# prepare MNIST
python prepare_dataset.py /raw_data/mnist mnist.zip --dataset mnist --portion train
```

### CIFAR-10 and CIFAR-100

[CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) 包含 10 个类别的 60,000 张图像。 其中，`train` 部分有 50,000 张图片，`test` 部分有 10,000 张图片。
[CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html) 则包含超过 100 个类别的 60,000 张图像。 其中，`train` 部分有 50,000 张图片，`test` 部分有 10,000 张图片。
请使用以下命令准备 CIFAR-10 和 CIFAR-100 数据集：

```shell
# prepare CIFAR-10
python prepare_dataset.py /raw_data/cifar10 cifar10.zip --dataset cifar10 --portion train

# prepare CIFAR-100
python prepare_dataset.py /raw_data/cifar100 cifar100.zip --dataset cifar100 --portion train
```

### LSUN

[LSUN](https://www.yf.io/p/lsun) 无法自动下载。 因此，请先手动下载并解压缩以获取 LMDB 数据库。 解压后文件结构应该是这样的：

```shell
$ tree -L 2 /raw_data/lsun  # layout of LSUN raw data

/raw_data/lsun
├── church_outdoor_train_lmdb
│   ├── data.mdb
│   └── lock.mdb
└── conference_room_train_lmdb
    ├── data.mdb
    └── lock.mdb
...
```

LSUN 数据集的统计信息如下：

| LSUN Datasets Stats | | |
| :-- | :--: | :--: |
| 名称 | 样本数 | 大小 |
| *Scenes*
| bedroom (train)         |  3,033,042 |  43 GB
| bridge (train)          |    818,687 |  15 GB
| church outdoor (train)  |    126,227 |   2 GB
| classroom (train)       |    168,103 |   3 GB
| conference room (train) |    229,069 |   4 GB
| dining room (train)     |    657,571 |  11 GB
| kitchen (train)         |  2,212,277 |  33 GB
| living room (train)     |  1,315,802 |  21 GB
| restaurant (train)      |    626,331 |  13 GB
| tower (train)           |    708,264 |  11 GB
| *Objects*
| airplane                |  1,530,696 |  34 GB
| bicycle                 |  3,347,211 | 129 GB
| bird                    |  2,310,362 |  65 GB
| boat                    |  2,651,165 |  86 GB
| bottle                  |  3,202,760 |  64 GB
| bus                     |    695,891 |  24 GB
| car                     |  5,520,756 | 173 GB
| cat                     |  1,657,266 |  42 GB
| chair                   |  5,037,807 | 116 GB
| cow                     |    377,379 |  15 GB
| dining table            |  1,537,123 |  48 GB
| dog                     |  5,054,817 | 145 GB
| horse                   |  2,000,340 |  69 GB
| motorbike               |  1,194,101 |  42 GB
| person                  | 18,890,816 | 477 GB
| potted plant            |  1,104,859 |  43 GB
| sheep                   |    418,983 |  18 GB
| sofa                    |  2,365,870 |  56 GB
| train                   |  1,148,020 |  43 GB
| tv monitor              |  2,463,284 |  46 GB

**注：LSUN 每个数据集都有 `train`、`val` 和 `test` 部分。 目前，仅支持场景 (Scenes) 数据集的准备。**

若要准备一个包含 `bedroom` 的训练集，可以使用命令：

```shell
python prepare_dataset.py /raw_data/lsun lsun_bedroom_train.zip --dataset lsun --portion bedroom_train
```

如准备一个同时包含 `tower_train` 和 `church_outdoor_train` 的图像数据集，可以使用命令:

```shell
python prepare_dataset.py /raw_data/lsun lsun_tower_church_train.zip --dataset lsun --portion 'conference_room_train,church_outdoor_train'
```

### ImageNet 1K

[ImageNet1k](http://www.image-net.org/) 由 1,281,167 个训练样本、50,000 个验证样本和 100,100 个超过 1,000 个类别的测试样本组成。 由于许可证的原因，用户应手动下载 ImageNet1k（例如，`ILSVRC2012_img_train.tar` (138 GB)）和 devkit（即，`ILSVRC2012_devkit_t12.tar.gz` (2.5 MB)）。 下载后文件结构应该是这样的：

```shell
$ tree -L 1 /raw_data/imagenet1k  # layout of ImageNet raw data

/raw_data/imagenet1k
├── ILSVRC2012_devkit_t12.tar.gz
└── ILSVRC2012_img_train.tar
```

可以用以下命令准备 ImageNet1k 的训练数据：

```shell
python prepare_dataset.py /raw_data/imagenet1k imagenet1k_train.zip --dataset imagenet1k --portion train
```

**注意：请确保磁盘至少有 414 GB 可用空间来为 ImageNet 准备 `train` 部分。**

### iNaturalist

[iNaturalist](https://github.com/visipedia/inat_comp) 收集了精细的大自然物种的图像。
对于 iNaturalist2021，它包含 2,686,843 个训练样本、500,000 个迷你训练样本、100,000 个验证样本和超过 10,000 个物种的 500,000 个测试样本。
我们的工具可以自动下载此数据集的不同版本。

```shell
python prepare_dataset.py /raw_data/inatrualist iNaturalist_2021_train.zip --dataset inaturalist --portion 2021_train
```

iNaturalist 的可用部分 (`--portion`) 有：`2017`、`2018`、`2019`、`2021_train`、`2021_train_mini` 和 `2021_valid`。

**注意：准备 iNaturalist 的 `2021_train` 需要 `torchvision>=0.11` 和至少 1.4 TB 可用空间。**

### 从自定义的文件夹打包数据

假设你在文件夹下有一个 3 类图像集合 /raw_data/customized_dataset`:

```shell
$ tree -L 1 /raw_data/customized_dataset  # layout of customized data

/raw_data/customized_dataset
├── class1
│   ├── img00000000.png
│   ├── ...
│   └── img00000010.png
├── class2
│   ├── img00000000.png
│   ├── ...
│   └── img00000012.png
└── class3
    ├── img00000000.png
    ├── ...
    └── img00000011.png
```

请使用以下命令准备你自己的数据：

```shell
python prepare_dataset.py /raw_data/customized_dataset custom.zip --dataset folder
```
