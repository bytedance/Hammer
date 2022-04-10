# Profile Your Model

Hammer integrates [torch.profiler](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html) to do profiling.

Adding `--enable_profiler=True` and starting the job as usual to enable profiling.

The following parameters are available if you need to make special adjustments during testing:

- `profiler_schedule_wait`: the number of steps/iters to wait before profiling;
- `profiler_schedule_warmup`: The number of steps/iters for performance analysis warmup, during this period, some profile overhead will be performed, performance analysis will be performed but it will not be recorded in the log;
- `profiler_schedule_active`: the number of steps/iters that actually perform performance analysis, and the operations during this period will be saved in the performance analysis record;
- `profiler_schedule_repeat`: how many times to repeat warmup to active;

Turning on the performance analysis itself will affect the performance of training, so it is only for reference.

Reference for the detailed information meaning in PYTORCH_PROFILER: https://github.com/pytorch/kineto/blob/main/tb_plugin/README.md