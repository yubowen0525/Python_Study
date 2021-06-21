# Future
使用future处理并发：futures.ThreadPoolExecutor()

Python3.4起， 标准库中有两个名为Future的类：concurrent.futures.Future 和 asyncio.Future。

两个Future类的实例都表示可能已经完成或者尚未完成的延迟计算。

我们需要记住：**通常情况下自己不应该创建future，而只能由并发框架(concurrent.futures 或 asyncio)实例化。**

原因很简单：future表示终将发生的事情，而确定某件事会发生的唯一方法是执行的时间已经排定。例如：Exector.submit()方法的参数是一个可调用的对象，调用这个方法后会传入的可调用
对象排期，并返回一个future。

future都有.done()方法，这个方法不阻塞，返回值是布尔值，指明future链接的可调用对象
是否已经执行。客户端代码不会询问future是否运行结束，而是等待通知。两个类都有.add_done_callback()方法：这个方法只有一个参数，类型是可调用的对象，future运行结束后调用指定的可调用对象。

## 重点
CPython解释器本身不是线程安全的，所以加入GIL(全局结束起锁的影响)，导致Python线程无法真正并发，所以一个进程只能使用一个线程。

但是Python在执行系统调用的时候，会释放GIL，达到并发的效果。

**所以在I/O密集型的工作中，使用线程池futures.ThreadPoolExecutor()，能达到真正并发的效果。**

**而CPU密集型作业上，因为没有系统调用，所以使用进程池futures.ProcessPoolExector()，达到真正的并发效果。**

## 使用
executor.map
1. executor.map = executor.submit + executor.as_completed
2. executor.map 使用方便，保证调用顺序返回。
3. 但会按future的顺序等待返回，效率不算太高
```
with futures.ThreadPoolExecutor(worker) as executor:
    # download_one 函数， cc_list 参数
    res = executor.map(download_one, sorted(cc_list))
```

executor.submit
1. executor.submit + executor.as_completed
2. 哪个future完成，futures.as_completed(to_do)就返回哪个，不会按照调用顺序返回，效率更高。
3. 但没有execuot.map方便。不保证future返回值的有序性。
```
with futures.ThreadPoolExecutor(worker) as executor:
    to_do = []
    for cc in sorted(cc_list):
        future = executor.submit(download_one, cc)
        to_do.append(future)
        msg = 'Scheduled for {}:{}'
        print(msg.format(cc, future))

    results = []
    for future in futures.as_completed(to_do):
        res = future.result()
```