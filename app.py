import redis
from redis_lru import RedisLRU
import functools
import time

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        runtime = time.perf_counter() - start
        print(f"{func.__name__} took {runtime:.4f} secs")
        return result
    return _wrapper


@timer
@cache
def fib_cache(n):
    if n <= 1:
        return n, 0
    else:
        (a, b) = fib_cache(n - 1)
        return a + b, a


if __name__ == '__main__':
    print(f'fib(10)={fib_cache(10)}')
    print(f'fib(10)={fib_cache(10)}')


