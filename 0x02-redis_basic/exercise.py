#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis())
and flushthe instance using flushdb.
"""
import redis
from typing import Union, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count_calls decorator that takes a single method
    Callable argument and returns a Callable
    use the qualified name of method using the __qualname__
    dunder method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        use the qualified name of method using the __qualname__
        dunder method.
        Increments key value by 1 on each function call
        """
        key = method.__qualname__
        self._redis.incr(key, amount=1)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    call_history is a decorator that takes in a
    single argument and returns a Callable
    store the history of inputs and outputs
    for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper takes in the exact parameter as method
        and records the in puts in a redis list
        It then calls the original function and
        records its outputs in another redis list
        """
        key_in = method.__qualname__+":inputs"
        key_out = method.__qualname__+":outputs"
        self._redis.rpush(key_in, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(key_out, res)
        return res
    return wrapper


def replay(method: Callable) -> None:
    """
    gets the the count and the inputs and outputs for each
    method call that is passed into it
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_inst = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_inst, redis.Redis):
        return
    key = method.__qualname__
    count = 0
    if redis_inst.exists(key) != 0:
        count = int(redis_inst.get(key))
    print("{} was called {} times".format(key, count))

    key_in = key+":inputs"
    key_out = key+":outputs"
    inputs = redis_inst.lrange(key_in, 0, -1)
    outputs = redis_inst.lrange(key_out, 0, -1)

    for inp, out in zip(inputs, outputs):
        i = inp.decode('utf-8')
        print("{}(*{}) -> {}:".format(key, i, out))


class Cache:
    """
    defines cache class that initializes
    redis instance and caches a result
    """
    def __init__(self) -> None:
        """
        initializes a redis object and usess
        flushdb to delete all keys in the
        current db
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores data into redis with a key that
        is of type uuid.uuid4
        return a uuid str
        """
        rnd_key = uuid.uuid4()
        self._redis.set(str(rnd_key), data)
        return str(rnd_key)

    def get(self, key: str, fn: Callable = None) ->\
            Union[str, bytes, int, None]:
        """
        This callable will be used to convert the data
        back to the desired format.
        Remember to conserve the original Redis.get behavior
        if the key does not exist.
        """
        v = self._redis.get(key)
        if v is None:
            return None
        if fn is not None:
            return fn(v)
        return v

    def get_str(self, key: str) -> Union[str, bytes, None]:
        """
        auto parametize cache.get with the correct
        coversion function for str type
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: int) -> Union[int, bytes, None]:
        """
        auto parametize cache.get with the correct
        coversion function for int type
        """
        return self.get(key, fn=int)
