import random

from typing import List
from operators.utils import tournament


def random_pick(items: List, size: int) -> None:
    pool = random.sample(items, size)
    for item in pool:
        item.is_alive = False


def fitness_tournament(items: List, size: int) -> None:
    pool = tournament(items, [-item.fitness for item in items], size)
    for item in pool:
        item.is_alive = False


def age_tournament(items: List, size: int) -> None:
    pool = tournament(items, [item.age for item in items], size)
    for item in pool:
        item.is_alive = False
