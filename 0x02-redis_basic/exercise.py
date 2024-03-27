#!/usr/bin/env python

"""
Module for defining a Cache class for storing data in Redis.
"""

import uuid
import redis


class Cache:
    def __init__(self):
        """
        Initializes a Cache object with a Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis with a randomly generated key.
        
        Args:
            data: The data to be stored in the cache. Can be a str, bytes, int, or float.
        
        Returns:
            str: The randomly generated key used for storing the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
