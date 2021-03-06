**序列构成的数组**

- [1. 内置序列类型概览](#1-内置序列类型概览)
- [2. 列表推导和生成器表达式](#2-列表推导和生成器表达式)
- [3. 元组不仅仅是不可变的列表](#3-元组不仅仅是不可变的列表)
  - [3.1. 具名元组](#31-具名元组)
  - [3.2. 3.2 不可变性](#32-32-不可变性)
- [4. 切片](#4-切片)
- [5. 序列的增量赋值](#5-序列的增量赋值)
- [6. list.sort 和 sorted](#6-listsort-和-sorted)
- [7. 用bisect来管理已排序的序列](#7-用bisect来管理已排序的序列)
- [8. 当列表不是首选](#8-当列表不是首选)
  - [8.1. 数组](#81-数组)
  - [8.2. 内存视图](#82-内存视图)
  - [8.3. NumPy 和 Scipy](#83-numpy-和-scipy)
  - [8.4. 双向队列和其他形式的队列](#84-双向队列和其他形式的队列)
    - [8.4.1. collections.deque](#841-collectionsdeque)
    - [8.4.2. queue](#842-queue)
    - [8.4.3. multiprocessing](#843-multiprocessing)
    - [8.4.4. asyncio](#844-asyncio)
    - [8.4.5. heapq](#845-heapq)

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

## 3.2. 3.2 不可变性
除了跟增删元素相关的方法之外，元组支持列表的其他所有方法。

# 4. 切片
切片的基本原则  [first:end:step] 其中step可以是负数，若为负数，则倒叙遍历。


# 5. 序列的增量赋值
[demo](./tuple.ipynb)

+= 调用的都是 `__iadd__` or `__imul__` 方法， 但是tuple 因为不可变性，没有`__iadd__`方法会转为调用 `__add__`，id 会改变。 list的id不会变，会改变自身

# 6. list.sort 和 sorted
list.sort 会返回 None

sorted函数返回 一个新的列表

[demo](./sort.ipynb)

# 7. 用bisect来管理已排序的序列
bisect 利用二分查找算法对有序列表进行 查找和插入

bisect.bisect(list, value) 返回 position

bisect.insort(list, value) 直接二分插入value元素。

# 8. 当列表不是首选
## 8.1. 数组
不像list, 数组array只能存放一种类型的对象， 且是字节表述，所以效率更高。

例如：array('b'), 创建的数组只存放一个字节大小的整数，当序列很大时能节省很多空间。

## 8.2. 内存视图
memoryview是一个内置类， 它能让用户在不复制内容的情况下操作同一个数组的不同切片

[demo](./memoryview.ipynb)


## 8.3. NumPy 和 Scipy
NumPy：提供高阶数组和矩阵操作

SciPY：专为线性代数、数值积分和统计学设计

Pandas：数据分析 以 Numpy为基础

Blaze：数据分析库

## 8.4. 双向队列和其他形式的队列
### 8.4.1. collections.deque
collections.deque 类 双向队列是一个线程安全，可以快速从两端添加或者删除元素的数据类型。

[demo](./deque.ipynb)

### 8.4.2. queue

提供了同步（线程安全）类 Queue、LifoQueue 和 PriorityQueue， 不同的线程可以利用这些数据类型来交换数据。

设置了 **maxsize** ， 当队列满了，它会被锁住，直到另外的线程移除了某个某个元素，腾出位置来。

### 8.4.3. multiprocessing
这个包实现了自己的Queue， 它跟queue.Queue类似，是设计给进程间通信用的。同时还有一个专门的multiprocessing.JoinableQueue类型，可以让任务管理变得更方便。

### 8.4.4. asyncio
异步包，里面有Queue、LifoQueue、PriorityQueue 和 JoinableQueue

### 8.4.5. heapq
heappush、 heappop，让用户把可变序列可以当作堆队列和优先队列来使用。