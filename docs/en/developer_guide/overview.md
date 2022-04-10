# Overview

## Recommended Procedure of Development

1. [Write Models](model.md) to determine network structure and APIs;
2. [Write Dataset](dataset.md) to specify how to fetch and read data;
3. Write [Loss](loss.md) to determine the optimization goal and use [Metrics](metric.md) as the evaluation index;
4. Write [Runner](runner.md) and [Config](config.md) to connect everything for debugging;
5. After determining the optimal parameters, write a demo and put it under `scripts/`;
6. If needed, you may also [write a Controller](controller.md) to perform some routine tasks during training;
7. If you concern the efficiency, you can [use profiler](profile.md) to test.
