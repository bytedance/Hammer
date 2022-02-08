# Dataset Preparation

We provide a tool, `prepare_dataset.py`, for dataset preparation. Considering the efficiency, `zip` format is recommended and consequently used. In particular, the script will collect all images inside a dataset and save them into a ZIP file. In addition, the script may also save the metadata (e.g., original filename) of the dataset and generate a simple annotation file, which pairs each image with a label.

**NOTE: Raw images are saved in the dataset without any pre-processing.**

## Format of the dataset

Generally, the layout of the dataset created by `prepare_dataset.py` is as follows

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
  6302822  2021-12-09 10:43   annotation.json  (annotation file)
---------                     -------
67698819325                     229070 files
```

Here, the annotation file looks like

```shell
[["0/img0.png", 0], ["0/img1.png", 0], ..., ["99/img229068.png", 99]]
```

## Usage

### Convert from a dataset created by StyleGAN2-ADA

If you have already had a dataset prepared with the official `dataset_tool.py` from [StyleGAN2-ADA](https://github.com/NVlabs/stylegan2-ada-pytorch) repository, it will be super-easy to convert it to get compatible with this repository. Basically, both repos use zipped dataset. Hence, we simply convert the annotation file. Please refer to `prepare_dataset.py` for more details.

The conversion can be achieved with the following command

```shell
python prepare_dataset.py /stylegan2ada/data.zip _unused --dataset 'stylegan2ada'
```

**NOTE: The script will add a new annotation file into the existing dataset instead of creating a new one.**

### Create a dataset from scratch

Generally, a dataset can be created with the following command

```shell
python prepare_dataset.py \
    ${PATH_TO_RAW_DATA} \
    ${SAVE_PATH} \
    --dataset ${DATASET_NAME} \
    --portion ${PORTION}
```

Here,

- `${PATH_TO_RAW_DATA}` is the path to the input dataset. For downloadable datasets, it can point to an empty folder.
- `${SAVE_PATH}` is the path to the output dataset with `zip` format.
- `${DATASET_NAME}` is either one of `cifar10`, `cifar100`, `mnist`, `imagenet1k`, `lsun`, `inaturalist`, or `folder` to make a dataset from a customized image collection.
- `${PORTION}` is the dataset portion. For example, for `imagenet1k`, the available portions are 'train', 'test', and 'val'.

## Dataset Description

Here, we provide basic description of some public datasets.

### MNIST

[MNIST](http://yann.lecun.com/exdb/mnist/) consists of 60,000 images, with 50,000 for `train` portion and 10,000 for `test` portion. Please use the following command to prepare the MNIST dataset.

```shell
# prepare MNIST
python prepare_dataset.py /raw_data/mnist mnist.zip --dataset mnist --portion train
```

### CIFAR-10 and CIFAR-100

[CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) consists of 60,000 images over 10 categories. Among them, there are 50,000 images for `train` portion and 10,000 for `test` portion. [CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html) consists of 60,000 images over 10 categories. Among them, there are 50,000 images for `train` portion and 10,000 for `test` portion. Please use the following commands to prepare the CIFAR-10 and CIFAR-100 dataset.

```shell
# prepare CIFAR-10
python prepare_dataset.py /raw_data/cifar10 cifar10.zip --dataset cifar10 --portion train

# prepare CIFAR-100
python prepare_dataset.py /raw_data/cifar100 cifar100.zip --dataset cifar100 --portion train
```

### LSUN

[LSUN](https://www.yf.io/p/lsun) cannot be automatically downloaded. Hence, please first download it manually and unzip it to get the LMDB database. After unzipping, the file structure should look like

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

In summary, the statistical information of LSUN dataset is

| LSUN Datasets Stats | | |
| :-- | :--: | :--: |
| Name | Number of Samples | Size |
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

**NOTE: Each dataset have `train`, `val`, and `test` portion. Currently, only Scenes are supported.**

To prepare a dataset for bedroom training set, please use command

```shell
python prepare_dataset.py /raw_data/lsun lsun_bedroom_train.zip --dataset lsun --portion bedroom_train
```

To prepare a dataset containing images from both `tower_train` and `church_outdoor_train`, please use command

```shell
python prepare_dataset.py /raw_data/lsun lsun_tower_church_train.zip --dataset lsun --portion 'conference_room_train,church_outdoor_train'
```

### ImageNet 1K

[ImageNet1k](http://www.image-net.org/) consists of 1,281,167 training samples, 50,000 validation samples, and 100,100 testing samples over 1000 classes. Due to the license, users should download ImageNet 1K (e.g., `ILSVRC2012_img_train.tar` (138 GB)) and the devkit (i.e., `ILSVRC2012_devkit_t12.tar.gz` (2.5 MB)) manually. After downloading, the file structure should look like

```shell
$ tree -L 1 /raw_data/imagenet1k  # layout of ImageNet raw data

/raw_data/imagenet1k
├── ILSVRC2012_devkit_t12.tar.gz
└── ILSVRC2012_img_train.tar
```

To prepare the dataset, please use the command

```shell
python prepare_dataset.py /raw_data/imagenet1k imagenet1k_train.zip --dataset imagenet1k --portion train
```

**NOTE: Please make sure the disk has at least 414 GB free space to prepare `train` portion for ImageNet.**

### iNaturalist

[iNaturalist](https://github.com/visipedia/inat_comp) collects images on natural fine-grained categories.
For iNaturalist2021, it contains 2,686,843 training samples, 500,000 mini training samples, 100,000 validation samples, and 500,000 testing samples over 10,000 species.
Different versions of this dataset can be downloaded automatically.

```shell
python prepare_dataset.py /raw_data/inatrualist iNaturalist_2021_train.zip --dataset inaturalist --portion 2021_train
```

Available portions of iNaturalist are: `2017`, `2018`, `2019`, `2021_train`, `2021_train_mini` and `2021_valid`.

**Note: Preparing iNaturalist requires `torchvision>=0.11` and at least 1.4 TB free space for `2021_train` portion.**

### Folder with customized image collection

Assume you have a 3-classes image collection under folder /raw_data/customized_dataset`:

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

Please use the following command to prepare your own data

```shell
python prepare_dataset.py /raw_data/customized_dataset custom.zip --dataset folder
```
