# 协程

[demo](./yield.ipynb)

1. yield 应被看作一种流程控制的工具，也可以看做是一个数据流通道 
2. 因为每次都需要next(coroutine) 对协程进行激活，所以可以写一个装饰器，在调用函数时，执行return next(func) 激活协程。
3. yield form 主要作为委派生成器，像管道一样委派数据给子生成器。 [demo](./yield.ipynb#子生成器)