import random

from typing import List


def single_point(a: List[float], b: List[float]) -> (List[float], List[float]):
    if len(a) != len(b):
        raise ValueError('chromosome length should be same')

    if len(a) <= 1:
        return a[:], b[:]

    point = random.randint(1, len(a) - 1)
    return (
        a[:point] + b[point:],
        b[:point] + a[point:]
    )


def blend(a: List[float], b: List[float]) -> (List[float], List[float]):
    pass


def simulated_binary(a: List[float], b: List[float]) -> (List[float], List[float]):
    pass

