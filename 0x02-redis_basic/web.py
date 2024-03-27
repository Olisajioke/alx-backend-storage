#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

cache_redis = redis.Redis()


def count_calls(func: Callable) -> Callable:
    '''Decorator function counts the number of times a function is called.'''
    @wraps(func)
    def wrapper(url) -> str:
        '''function that counts calls(Wrapper function)'''
        cache_redis.incr(f'count:{url}')
        result = cache_redis.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = func(url)
        cache_redis.set(f'count:{url}', 0)
        cache_redis.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@count_calls
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
