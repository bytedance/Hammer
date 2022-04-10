# 概览

**注：** 开发前务必阅读项目中的 `CONTRIBUTING.md`.

## 推荐的项目开发顺序

1. 先 [编写模型 (Models)](model.md) 以确定网络结构；
2. 接着 [编写 Dataset](dataset.md) 规范数据的读取形式；
3. 编写 [Loss](loss.md) 确定优化目标，以及 [Metrics](metric.md) 作为评估指标；
4. 编写 [Runner](runner.md) 和 [Config](config.md) 联调项目；
5. 确定好最优参数后，写成模板放入 `scripts/` 下；
6. 如果有需要，你可能也会 [编写 Controller](controller.md) 在训练过程中定期执行一些任务；
7. 如果对性能有高要求，可以 [使用 profiler](profile.md) 测试。
