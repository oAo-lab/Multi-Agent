import asyncio
import functools


# 定义一个异步装饰器
def async_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = await asyncio.to_thread(func, *args, **kwargs)  # 在线程中运行普通函数
        print(f"After calling {func.__name__}")
        return result

    return wrapper


# 普通函数
def normal_function(x):
    print(f"Running normal_function with {x}")
    return x * 2


# 使用装饰器装饰普通函数
@async_decorator
def decorated_normal_function(x):
    return normal_function(x)


# 测试异步装饰器
async def main():
    result = await decorated_normal_function(5)
    print(f"Result: {result}")


asyncio.run(main())
