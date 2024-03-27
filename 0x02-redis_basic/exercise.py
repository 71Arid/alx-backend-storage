#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis())
and flushthe instance using flushdb.
"""
import redis
from typing import Union
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
