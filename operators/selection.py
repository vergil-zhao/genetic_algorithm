import random

from typing import List
from operators.utils import create_wheel, pick_from_wheel, tournament


def random_pick(items: List, size: int, **kwargs) -> List:
    """
    Randomly pick items to create a pool.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    return random.sample(items, size)


def roulette_wheel(items: List, size: int, **kwargs) -> List:
    """
    Pick item randomly at a roulette wheel of which width is the fitness value.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    wheel = create_wheel([item.fitness for item in items])
    return pick_from_wheel(items, wheel, size)


def fitness_tournament(items: List, size: int, **kwargs) -> List:
    """
    Pick item by rounds of tournament.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    return tournament(items, [item.fitness for item in items], size)


def rank(items: List, size: int, **kwargs) -> List:
    """
    Derived from roulette wheel, roulette created by rank number,
    the higher fitness value the rank number will be.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    items_sorted = sorted(items)
    length = len(items_sorted)

    wheel = create_wheel([i for i in range(1, length + 1)])
    return pick_from_wheel(items, wheel, size)
