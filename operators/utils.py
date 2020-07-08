import random

from typing import TypeVar, List
from copy import deepcopy

T = TypeVar('T')
S = TypeVar('S')


def print_name(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        func(*args, **kwargs)
    return wrapper


def prettify_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)


def create_wheel(items: List[T]) -> List[T]:
    assert len(items) > 0, 'items cannot be empty'

    wheel = [items[0]]
    for i in range(1, len(items)):
        wheel.append(wheel[-1] + items[i])
    return wheel


def pick_from_wheel(items: List[T], wheel: List[S], size: int) -> List[T]:
    assert len(items) == len(wheel), 'items and wheel should have same size'
    assert size <= len(items), 'size cannot be greater than items size'

    pool = []
    total = wheel[-1]
    for i in range(size):
        pick = random.random() * total
        j = 0
        while pick > wheel[j]:
            j += 1
        pool.append(deepcopy(items[j]))

    return pool


def tournament(items: List[T], values: List[S], size: int, round_size: int = 3) -> List[T]:
    assert len(items) == len(values), 'items and values should have same size'
    assert size <= len(items), 'size could not be greater than items size'

    remain = [i for i in range(len(items))]
    random.shuffle(remain)

    pool = []
    for i in range(size):
        if len(remain) < round_size:
            round_pool = remain
        else:
            round_pool = random.sample(remain, round_size)

        max_index = round_pool[0]
        max_value = values[round_pool[0]]
        for index in round_pool:
            if values[index] > max_value:
                max_value = values[index]
                max_index = index

        pool.append(items[max_index])
        remain.remove(max_index)

    return pool


def repair(genes: List[float]) -> List[float]:
    repaired = genes[:]
    for i in range(len(repaired)):
        repaired[i] %= 1
    return repaired
