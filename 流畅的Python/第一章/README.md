- [1. Python 数据模型](#1-python-数据模型)
  - [1.1. 一摞Python风格的纸牌](#11-一摞python风格的纸牌)
  - [1.2 如何使用特殊方法](#12-如何使用特殊方法)
  - [1.3 特殊方法一览](#13-特殊方法一览)

# 1. Python 数据模型
[标准库-数据模型](https://docs.python.org/zh-cn/3.6/reference/datamodel.html#data-model)
## 1.1. 一摞Python风格的纸牌

[collections_card.py](第一章/1.1/collections_card.py)


class 内的一些特殊函数, 若实现了这些方法就能使用标准库诸如 random.choice、reversed和sorted这些函数。
- `def __init__(self)` 构造函数
- `def __len__(self)`  使用内置`len()`函数呼出
- `def __getitem__(self)` 使用`[]`函数呼出，支持**切片**操作，支持**可迭代**的操作
- `def __setitem__(self)` 一旦实现，类内的属性就能被修改
- `def __contains__(self)`  若没有实现该方法，使用`in`运算符会按顺序做一次迭代

---
## 1.2 如何使用特殊方法

[math](第一章/1.2/math.py)

通过`__repr__`、`__abs__`、`__add__`、`__mul__`这些特殊方法实现数学计算。
- `__repr__` 直接打印对象，以字符串的形式表达出来以便辨认，更类似对象构造器的表达形式。**应表述准确、无误！**
- `__str__`它被`str()`函数使用，在`print()`一个对象时调用。
- 若没有`__str__` 方法， Python又需要调用解释器会用`__repr__`作为替代。

## 1.3 特殊方法一览
[标准库-数据模型](https://docs.python.org/zh-cn/3.6/reference/datamodel.html#data-model) 具体方法说明。

**跟运算符无关的特殊方法**：

类别 | 方法名
---------|----------
 字符串 /字节序列表示形式| `__repr__、__str__、__format__、__bytes__` 
 数值转换 | `__abs__、__bool__、__complex__、__int__、__float__、__hash__、__index__ `
 集合模拟 | `__len__、__getitem__、__setitem__、__delitem__、__contains__` 
 迭代枚举 | `__iter__、__reversed__、__next__`
 可调用模拟 | `__call__` 
 上下文管理 | `__enter__、__exit__` 
 属性管理| `__getattr__、__getattribute__、__setattr__、__delattr__、__dir__` 
 跟类相关的服务| `__prepare__、__instancecheck__、__subclasscheck__`  
