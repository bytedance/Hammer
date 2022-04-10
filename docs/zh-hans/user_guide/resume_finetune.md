# 恢复 (Resume) 与 微调 (Fine-tune)

> Resume 与 Fine-tune 的区别：
> - Resume 一般用于继续之前的实验，会将 网络参数、learning rate、optimizer 和训练时的统计量加载回来，要求使用的数据集也保持与之前实验一致；
> - Fine-tune 一般用于迁移学习，比如把训在 FFHQ 上的模型迁移到风格化的数据集上，只会将 网络参数 加载回来。

## Resume

只需在原有的参数后面加上 `--resume_path=<PATH_TO_CKPT>` 即可。当在开发机上训练时，此处应填写一个绝对路径。

## Fine-tune

只需在原有的参数后面加上 `--weight_path=<PATH_TO_CKPT>` 即可。当在开发机上训练时，此处应填写一个绝对路径。