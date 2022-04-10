# 性能测试

Hammer 集成了 [torch.profiler](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html) 进行性能测试。

训练时，加上 `--enable_profiler=True` 并按往常启动实验即可开启性能分析。

如果需要对测试的时期做特别的调整，有如下参数可选：

- `profiler_schedule_wait`：进行性能分析前等待的 step/iter 数；
- `profiler_schedule_warmup`：性能分析热身的 step/iter 数，在此期间的会进行一些 profile 的 overhead，进行性能分析但是不会记录到 log 里；
- `profiler_schedule_active`：真正进行性能分析的 step/iter 数，这段期间的操作会保存到性能分析记录中；
- `profiler_schedule_repeat`：将 warmup 至 active 这个再重复多少次；

开启性能分析本身会影响训练的性能，故仅作参考。

PYTORCH_PROFILER 中详细的信息含义参考：https://github.com/pytorch/kineto/blob/main/tb_plugin/README.md