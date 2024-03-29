#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of the
function is very simple. It uses the requests module to
obtain the HTML content of a particular URL and returns it.
"""
import requests
from functools import wraps
from typing import Callable
import redis


redis_inst = redis.Redis()
"""global instance of redis.
"""


def count_calls(method: Callable) -> Callable:
    """
    implements the count functionality recording each
    time a specific url is called
    """
    @wraps(method)
    def wrapper(url):
        redis_inst.incr(f"count:{url}")
        res = redis_inst.get(f"result:{url}")
        if res:
            return res.decode('utf-8')
        res = method(url)
        redis_inst.setex(f"result:{url}", 10, res)
        return res
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    use requests.get to get the contents from
    the url and then set expitation time of
    a cache value it input in redis
    """
    return requests.get(url).text
