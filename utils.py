import random

from typing import TypeVar, List
from copy import deepcopy


def prettify_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)


T = TypeVar('T')
S = TypeVar('S')


def create_wheel(items: List[T]) -> List[T]:
    wheel = [items[0]]
    for i in range(1, len(items)):
        wheel.append(wheel[-1] + items[i])
    return wheel


def pick_from_wheel(items: List[T], wheel: List[S], size: int) -> List[T]:
    pool = []
    total = wheel[-1]
    for i in range(size):
        pick = random.random() * total
        j = 0
        while pick > wheel[j]:
            j += 1
        pool.append(deepcopy(items[j]))

    return pool
