"""Deterministic generation of input sequences."""

import random

from .parser import Topic


def make_topic(
    *,
    name: str = "Number Search",
    count: int = 20,
    min_length: int = 8,
    max_length: int = 8,
    seed: int = 42,
) -> Topic:
    if count not in (15, 20) or not 6 <= min_length <= max_length <= 10:
        raise ValueError("Count must be 15 or 20; lengths must be between 6 and 10")
    rng = random.Random(seed)
    ordered: list[str] = []
    while len(ordered) < count:
        length = rng.randint(min_length, max_length)
        candidate = "".join(rng.choices("0123456789", k=length))
        if candidate not in ordered:
            ordered.append(candidate)
    return Topic(name, tuple(ordered))
