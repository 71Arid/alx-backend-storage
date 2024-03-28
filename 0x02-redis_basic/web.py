#!/usr/bin/python3
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


def count_calls(method: Callable) -> Callable:
    """
    implements the count functionality recording each
    time a specific url is called
    """
    @wraps(method)
    def wrapper(url):
        key = "count:{}".format(url)
        redis_inst = redis.Redis()
        redis_inst.incr(key, amount=1)
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    use requests.get to get the contents from
    the url and then set expitation time of
    a cache value it input in redis
    """
    redis_inst = redis.Redis()
    key = "result:{}".format(url)
    cached_res = redis_inst.get(key)
    if cached_res:
        return cached_res.decode('utf-8')
    else:
        resp = requests.get(url)
        redis_inst.setex(key, 10, resp.text)
        return resp.text
