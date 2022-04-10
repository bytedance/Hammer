# Overview

## Basic Concepts

* Model: defines the **network structure**.
* Runner: defines the standardized training **process**.
* Controller: plugins that are executed **periodically** in the process.

## Overview of Training Procedure

```{mermaid}

   stateDiagram-v2
   direction LR
   [*] --> Launch
   Launch --> Preprocess
   Preprocess --> Training(runner.train())
   Training(runner.train()) --> [*]
   state Launch {
      [*] --> run_some_demo_scripts
      run_some_demo_scripts --> `dist_train.sh`
      `dist_train.sh` --> Parse: Distributed from now on
      Parse --> [*]
      state Parse {
         [*] --> recognize_command
         recognize_command --> match_config: one config file for one command
         match_config --> update_configs_from_CLI
         update_configs_from_CLI --> [*]
      }
   }
   state Preprocess {
      [*] --> build_runner
      build_runner --> [*]
      
      state build_runner {
         [*] --> build_work_dir_and_logs
         build_work_dir_and_logs --> `prefetch_data()`
         `prefetch_data()` --> build_dataloaders
         build_dataloaders --> `build_models()`
         `build_models()` --> `build_optimizers()`
         `build_optimizers()` --> `build_lr_scheduler()`
         `build_lr_scheduler()` --> `build_loss()`
         `build_loss()` --> `build_controllers()`
         `build_controllers()` --> build_metrics
         build_metrics --> resume/finetune
         resume/finetune --> [*]
      }
   }
   state Training(runner.train()) {
      state if_end <<choice>>
      [*] --> prepare_profiler
      prepare_profiler --> `pre_execute_controllers()`
      `pre_execute_controllers()` --> get_next_batch_data
      get_next_batch_data --> iter_timer_starts
      iter_timer_starts --> `train_step()`
      `train_step()` --> iter_timer_ends
      iter_timer_ends --> `post_execute_controllers()`
      `post_execute_controllers()` --> if_end
      if_end --> `pre_execute_controllers()`: if unfinished
      if_end --> [*]: if finished
   }
```


## Some Default Behaviors to Be Aware of

1. In order to save storage space, Hammer will automatically clean up intermediate checkpoints. 
   By default, it reserves **the latest 20** checkpoints, you can also modify the number of reserved checkpoints to `<NUM>` by setting `--keep_ckpt_num=<NUM>`, if `<NUM>` is `-1 ` then keep all intermediate checkpoints.
   
2. For image data, if the original resolution is inconsistent with the training resolution, it will automatically be **center cropped and then scaled** to the training resolution.

3. Hammer uses `--job_name` to distinguish jobs and build work directories. In order to avoid accidental overwriting, an error will be raised directly when encountering an existed directory.