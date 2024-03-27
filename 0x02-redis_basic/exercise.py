#!/usr/bin/env python

"""Module for defining a Cache class for storing data in Redis."""

import uuid
import redis
from typing import Callable, Union


class Cache:
    def __init__(self):
        """Initializes a Cache object with a Redis client and flushes the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the input data in Redis with a randomly generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieves data from Redis with the specified key and applies the conversion function if provided."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieves data from Redis with the specified key and returns it as a UTF-8 decoded string."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieves data from Redis with the specified key and returns it as an integer."""
        return self.get(key, fn=int)
