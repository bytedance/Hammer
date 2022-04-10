# Resume and Fine-tune

> Difference between Resume and Fine-tune:
> - `Resume` is generally used to continue a previous experiment, and will load the network weights, learning rate, optimizer and statistics back, and the required data set should be consistent with the previous experiment;
> - `Fine-tune` is generally used for transfer learning, such as transferring a model trained on FFHQ to a stylized dataset, and only loading the network parameters back.

## Resume

Simply adding `--resume_path=<PATH_TO_CKPT>` to resume a job. When training on a devbox, an absolute path should be filled in here.

## Fine-tune

Simply adding `--weight_path=<PATH_TO_CKPT>` to fine-tune a model. When training on a devbox, an absolute path should be filled in here.