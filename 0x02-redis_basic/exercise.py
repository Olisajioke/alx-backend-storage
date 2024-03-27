#!/usr/bin/env python
"""Module for defining a Cache class for storing data in Redis."""

import uuid
import redis
import functools
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Store input arguments
        self._redis.rpush(input_key, str(args))
        
        # Execute the wrapped function
        result = method(self, *args, **kwargs)
        
        # Store output
        self._redis.rpush(output_key, result)
        
        return result
    return wrapper


def replay(method_name: str):
    """Display the history of calls for a particular function."""
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"History of calls for method '{method_name}':")
    for i, (input_data, output_data) in enumerate(zip(inputs, outputs), 1):
        print(f"Call {i}: Input: {input_data}, Output: {output_data}")


class Cache:
    def __init__(self):
        """Initializes a Cache object with a Redis client and flushes the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the input data in Redis with a randomly generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    

     def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves data from Redis with the specified key 
        and applies the conversion function if provided."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieves data from Redis with the specified key and
        returns it as a UTF-8 decoded string."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieves data from Redis with the specified key
        and returns it as an integer."""
        return self.get(key, fn=int)