# 概览

## 概念解释

* Model：定义了 **网络结构**，只关注模型本身。
* Runner：定义了规范化的训练 **流程**。
* Controller：一些在流程中 **定期执行的插件**。

## 训练流程

```{mermaid}

   stateDiagram-v2
   direction LR
   [*] --> 启动
   启动 --> 预处理
   预处理 --> 训练(runner.train())
   训练(runner.train()) --> [*]
   state 启动 {
      [*] --> 由scripts/下的脚本启动
      由scripts/下的脚本启动 --> 由dist_train.sh启动
      由dist_train.sh启动 --> 解析配置: 从这一步开始分布式
      解析配置 --> [*]
      state 解析配置 {
         [*] --> 识别command
         识别command --> 调取config: 一个config文件对应一个command
         调取config --> 从终端解析并更新配置
         从终端解析并更新配置 --> [*]
      }
   }
   state 预处理 {
      [*] --> 构建runner
      构建runner --> [*]
      
      state 构建runner {
         [*] --> 构建工作路径和日志相关工具
         构建工作路径和日志相关工具 --> 拉取数据
         拉取数据 --> 构建dataloader
         构建dataloader --> 构建models
         构建models --> 构建optimizers
         构建optimizers --> 构建学习率调节器
         构建学习率调节器 --> 构建loss
         构建loss --> 构建controller
         构建controller --> 构建metrics
         构建metrics --> 从checkpoint恢复或微调
         从checkpoint恢复或微调 --> [*]
      }
   }
   state 训练(runner.train()) {
      state if_end <<choice>>
      [*] --> 准备性能测试工具
      准备性能测试工具 --> `pre_execute_controllers()`
      `pre_execute_controllers()` --> 取出下一个批次训练数据
      取出下一个批次训练数据 --> iter计时开始
      iter计时开始 --> `train_step()`
      `train_step()` --> iter计时结束
      iter计时结束 --> `post_execute_controllers()`
      `post_execute_controllers()` --> if_end
      if_end --> `pre_execute_controllers()`: 若训练未结束
      if_end --> [*]: 若训练结束
   }
```


## 一些需要注意的默认行为

1. 为了节约存储空间，Hammer 会自动清理中间节点（checkpoints）。
   默认保留的节点数为 **最近 20 个**，你也可以通过设置 `--keep_ckpt_num=<NUM>` 修改保留的节点数为 `<NUM>`，若 `<NUM>` 为 `-1` 则保留全部中间节点。
   
2. 对于图片数据，若原始分辨率与训练分辨率不一致，会自动 **先中心裁切再缩放** 到训练分辨率。

3. Hammer 使用 `--job_name` 来区分实验并构建工作路径，为避免意外覆盖，遇到同名路径会直接报错提示。