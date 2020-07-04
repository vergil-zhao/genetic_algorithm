import random

from typing import List
from genetic import Chromosome
from utils import create_wheel, pick_from_wheel


def random_pick(items: List[Chromosome], size: int) -> List[Chromosome]:
    return random.sample(items, size)


def roulette_wheel(items: List[Chromosome], size: int) -> List[Chromosome]:
    """
    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    wheel = create_wheel([item.fitness for item in items])
    return pick_from_wheel(items, wheel, size)


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


def rank(items: List[Chromosome], size: int) -> List[Chromosome]:
    """
        :param items: list of chromosome, fitness value has to be positive
        :param size: the mating mating pool
        :return: the mating pool
    """
    items_sorted = sorted(items)
    length = len(items_sorted)

    wheel = create_wheel([i for i in range(1, length + 1)])
    return pick_from_wheel(items, wheel, size)
