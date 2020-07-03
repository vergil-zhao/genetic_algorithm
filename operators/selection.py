import random

from copy import deepcopy
from functools import reduce
from typing import List
from genetic import Chromosome


def random_pick(items: List[Chromosome], size: int) -> List[Chromosome]:
    return random.sample(items, size)


def roulette_wheel(items: List[Chromosome], size: int) -> List[Chromosome]:
    total = reduce(lambda s, x: s + x.fitness, items, 0.0)
    wheel = [item.fitness for item in items]
    for i in range(1, len(wheel)):
        wheel[i] += wheel[i - 1]

    pool = []
    for i in range(size):
        v = random.random() * total
        j = 0
        while v > wheel[j]:
            j += 1
        pool.append(deepcopy(items[j]))

    return pool


TOURNAMENT_SIZE = 3


def tournament(items: List[Chromosome], size: int) -> List[Chromosome]:
    remain = items[:]
    random.shuffle(remain)

    pool = []
    for i in range(size):
        if len(remain) < TOURNAMENT_SIZE:
            round_pool = remain
        else:
            round_pool = [remain.pop() for _j in range(TOURNAMENT_SIZE)]

        pool.append(max(round_pool))

    return pool
