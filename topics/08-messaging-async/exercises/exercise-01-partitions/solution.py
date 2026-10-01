"""Solution: hash the key, deal the shelves."""

import hashlib


def partition(key, n):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % n


def assign(partitions: list, consumers: list):
    return {
        c: [p for i, p in enumerate(partitions) if i % len(consumers) == consumers.index(c)]
        for c in consumers
    }
