#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis())
and flushthe instance using flushdb.
"""
import redis
from typing import Union, Callable, Optional
import uuid


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

    def store(self, data: Union[int, float, bytes, str]) -> str:
        """
        stores data into redis with a key that
        is of type uuid.uuid4
        return a uuid str
        """
        rnd_key = uuid.uuid4()
        self._redis.set(str(rnd_key), data)
        return str(rnd_key)

    def get(self, key: str, fn: Optional[Callable]) -> Union[str, bytes, int, None]:
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


if __name__ == "__main__":
    cache = Cache()
    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
