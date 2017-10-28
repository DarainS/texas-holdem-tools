# texas-holdem-tools
A series Tools for texas hold'em with python. 

# Install

```python
    # install requirement
    git clone https://github.com/DarainS/texas-holdem-tools
    cd ./texas-holdem-tools
    pip3 install -r requirement.txt
```
```python
    # install mongodb
    # by Docker
    docker pull mongo
    and then mongo.py file would auto run mongodb by docker.
```

## Include

1. 牌力计算算法

2. 胜率计算器：蒙特卡洛随机与regular两种方式。

3. 牌力收敛功能。将169种牌的胜率不断收敛。



## Improve

1. 直接计算7张牌的牌力，相较于5张性能提高了30~40倍。

## Todo

- [ ] 考虑range的数据结构。
    - 翻前range：Axs,22+,Kxs,54s+,97s+等
- [ ] 如何较好的计算特定手牌的强度。
    - allin 强度，主要为面对3%、5%、7%、10%、13%、17%的range的期望胜率。
    - 翻后强度，主要有中牌率、中牌强度、摊牌胜率三个参数。
- [ ] 计算对手的range范围：对手中各种牌对应的组合与数目
- [ ] 面对对手的range范围的胜率

## Finish

- [x] 建立翻后result模型，数据格式为{level0:1,name0:高牌,num0:10,winNum0:6,rate0:0.1,winRate0:0.6,...}

## AI base Reforce Learning
1. 构建一个德扑的完整游戏
2. AI对所有的行为随机生成一个概率作为初始值
3. 对于每局比赛的收益加入到节点数据
4. 训练，查看训练结果
大神Hinton的Capsule论文终于公开，神经网络迎来新探索:[https://zhuanlan.zhihu.com/p/30521733](https://zhuanlan.zhihu.com/p/30521733)
RN:[https://www.zhihu.com/question/40554481](https://www.zhihu.com/question/40554481)
CapsNet:[https://mp.weixin.qq.com/s/8P-oRV9zAbaKRd1RJCN0Bg](https://mp.weixin.qq.com/s/8P-oRV9zAbaKRd1RJCN0Bg)

