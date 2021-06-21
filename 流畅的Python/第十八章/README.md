# python3.4 asyncio
asyncio包 异步包解决I/O的等待时间


用事件循环机制来驱动协程工作，此时1个线程内只有一个事件驱动。
```
loop = asyncio.get_event_loop()
result = loop.run_until_complete(1个协程或者1组协程)
loop.close()
```

若在事件驱动内，发生非asyncio包内的协程事件，会阻塞协程，例如：time.sleep(), 文件系统读写。

对协程来说，无需保留锁， 因为协程自身同步，在任意时刻只有一个协程工作，yield或者yield from把
控制权交还给调度程序。

当在协程内使用文件系统读写时，可以使用
```
loop = get_event_loop()
loop.run_in_exeuctor(none, func, *arg)
```
第一个参数是Executor实例，如果设置为None，使用事件循环默认ThreadPoolExecutor实例。


目前Python3.7已经优化了该包，async 和 await 协作。

# python3.7 asyncio


