**序列构成的数组**

- [1. 内置序列类型概览](#1-内置序列类型概览)
- [2. 列表推导和生成器表达式](#2-列表推导和生成器表达式)
- [3. 元组不仅仅是不可变的列表](#3-元组不仅仅是不可变的列表)
  - [3.1. 具名元组](#31-具名元组)

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

# 2. 列表推导和生成器表达式
**[demo](../第二章/listcomps_and_genexps.ipynb)**

列表推导主要用于构建列表的快捷方式

**生成器表达式则用来创建其他任何类型**


# 3. 元组不仅仅是不可变的列表
总结元组的两大功能：
1. 当作记录来用的数据结构
2. 充当一个不可变的列表


元组其实是对数据的记录， 每个元素都存放了一个字段的数据， **外加这个字段的位置**。

`*`运算符可以把一个可迭代对象拆开作为函数的参数。

可以用 `*` 来拆包， 承接剩下的元素

[demo](tuple.ipynb)

## 3.1. 具名元组
利用`collections.namedtuple`对元组的各个字段命名，转化像dict一样

[demo](tuple.ipynb)