**字典与集合**

- [1. 泛映射类型](#1-泛映射类型)
  - [1.1. 什么是可散列的数据结构](#11-什么是可散列的数据结构)
- [2. 字典推导](#2-字典推导)
- [3. 常用的映射方法](#3-常用的映射方法)
  - [3.1. setdefault 处理找不到的键](#31-setdefault-处理找不到的键)
- [4. 映射的弹性键查询](#4-映射的弹性键查询)
  - [4.1. defaultdict](#41-defaultdict)
  - [4.2. 特殊方法 __missing__](#42-特殊方法-missing)
- [5. 字典的变种](#5-字典的变种)
- [6. 子类化UserDict](#6-子类化userdict)
- [7. 不可变映射类型](#7-不可变映射类型)
- [8. 集合论](#8-集合论)
- [9. dict 和 set 的背后](#9-dict-和-set-的背后)

# 1. 泛映射类型
collections.abc 模块中有Mapping和MutableMapping这两个抽象基类，它们的作用是为dict和其他类似的类型定义形式接口。

## 1.1. 什么是可散列的数据结构
如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现 `__hash__()` 方法。另外可散列对象还要有 `__eq__()` 方法， 这样才能跟其他键做比较。

# 2. 字典推导
与list类似，不过这里应该是生成器推导

# 3. 常用的映射方法
除了dict，还有defaultdict和OrderedDict这两个dict变种，方便我们日常的使用。

说下 update：`d.update(m, [**kargs])`。函数首先检测m是否有keys()方法，如果有，那么update函数就把它作为映射对象来处理。否则，函数会进一步，转而把m当作包含了键值对(key, value)元素的迭代器。

## 3.1. setdefault 处理找不到的键
`d.setdefault(key, [default])` 若找不到key，会直接返回default值  

```python
my_dict.setdefault(key, []).append(new_value)

# 跟这样写一样

if key not in my_dict:
    my_dict[key] = []
my_dict[key].append(new_value)

```
下面的方法除了需要3行，而且还查询了2次key。


# 4. 映射的弹性键查询
## 4.1. defaultdict
[demo](./default.ipynb)

在实例化一个defaultdict，需要给构造方法提供一个可调用对象，这个可调用对象会在`__gettiem__`碰到找不到键时被调用，返回设置的默认值。

```
my_dict = defaultdict(list)
my_dict[keu].append(new_value)
```

> defaultdict里面的defalut_factory只会在 `__gettiem()__` 里被调用

## 4.2. 特殊方法 __missing__
所有映射类型在找不到key时，都会牵扯到 `__missing__` 方法。

如果一个类继承了dict并实现了missing方法，那么在gettiem找不到该key，会自动调用该missing方法，而不是抛出异常。

**需要注意的是，`__missing__` 方法对 `get` 和 `__contains__`(in 操作符) 并不起作用。**

# 5. 字典的变种
[demo](./default.ipynb)

**collections.OrderDict**
- 添加键的时候会保持顺序，因此键的迭代次序总是一致的。
- popitem() 默认删除并返回字典的最后一个元素， popitem(last=False) 那么删除并返回第一个被添加进去的元素
 
**collections.ChainMap**
- 容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到。
- 该功能在给有嵌套作用域的语言做解释器的时候很有作用
```python
import builtins

pylookup = ChainMap(locals(), globals(), vars(builtins))
```


**collections.Counter**
- 给键准备一个整数计时器, 每次更新一个键的时候都会增加这个计数器。
- 可用来给可散列对象计数
- +、-、most_common([n]) 

**collections.UserDict**
- 这个类其实就是把标准dict用纯Python又实现了一遍。
- 该类与其他开箱即用不同，它必须让用户继承写子类的
  

# 6. 子类化UserDict
相比于继承dict实现，继承UserDict是更好的选择。
- 其中有data属性，是dict的实例，好处是实现`__settiem__` 避免不必要的递归。
- UserDict继承MutableMapping， 所以UserDIct会继承MutableMapping、Mapping这些方法。

# 7. 不可变映射类型
有些映射类型数据并不希望使用者可以修改该数据，只希望是只读的数据。

Python3.3以后，types引入一个模块`MappingProxyType`, 该模块能解决此类问题。

[demo](./default.ipynb)

# 8. 集合论
集合就是 set（可变，无序） 或是 frozenset（冻结set，不可变） ， 集合首先保证了唯一性。

[demo](./set.ipynb)

方便的集合操作：
- a ｜ b ： 并集
- a  & b ： 交集
- a - b ： 差集

# 9. dict 和 set 的背后
回答以下几个问题：
- Python里的dict和set的效率有多高？
- 为什么它们是无序的？
- 为什么并不是所有的Python对象都可以当作dict的键或set里的元素？
- 为什么dict的键和set元素的顺序是根据它们被添加的次序而定的，以及为什么在映射对象的生命周期内，顺序并不是一尘不变的。
- 为什么不应该在迭代循环dict或是set的同时往里面添加元素？