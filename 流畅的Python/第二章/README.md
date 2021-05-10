**序列构成的数组**

- [1. 内置序列类型概览](#1-内置序列类型概览)
- [列表推导和生成器表达式](#列表推导和生成器表达式)

# 1. 内置序列类型概览

Python标准库用C实现了丰富的序列类型，列举如下：

**容器序列：能存放不同类型的数据**
- list
- tuple
- collections.deque

**扁平序列：只能容纳一种类型**
- str
- bytes
- bytearray
- memoryview
- array.array

**可变序列：**
- list
- bytearray
- array.array
- collections.deque
- memoryview

**不可变序列:**
- tuple
- str
- bytes

# 列表推导和生成器表达式
**[demo](../第二章/listcomps_and_genexps.ipynb)**

列表推导主要用于构建列表的快捷方式

**生成器表达式则用来创建其他任何类型**