## AI base Reforce Learning
1. 构建一个德扑的完整游戏
2. AI对所有的行为随机生成一个概率作为初始值
3. 对于每局比赛的收益加入到节点数据
4. 训练，查看训练结果
- 大神Hinton的Capsule论文终于公开，神经网络迎来新探索:[https://zhuanlan.zhihu.com/p/30521733](https://zhuanlan.zhihu.com/p/30521733)
- RN:[https://www.zhihu.com/question/40554481](https://www.zhihu.com/question/40554481)
- CapsNet:[https://mp.weixin.qq.com/s/8P-oRV9zAbaKRd1RJCN0Bg](https://mp.weixin.qq.com/s/8P-oRV9zAbaKRd1RJCN0Bg)

## Basic Algorithm

### 决策
check
bet 0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.2,1.5,1.8,2.0,2.5,3.0,4.0+
call
fold


### 算法策略
构建4个不同的神经网络，分别计算四个部分的权重。
玩家初始化神经网络。
输钱的策略减少权重，反向更新。


## Compose

### 桌面数据
位置，有效筹码
### 玩家形象
玩家过去的行为
### 玩家行为-牌力阅读
玩家本手牌的行为
### 自身牌力
当前牌力，潜在牌力；对方牌力组合，对方潜在牌力组合
### 行为决策

