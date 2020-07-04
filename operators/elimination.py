import random

from typing import List
from genetic import Chromosome


def random_pick(items: List[Chromosome], size: int) -> None:
    pool = random.sample(items, size)
    for item in pool:
        item.is_alive = False


def fitness_tournament(items: List[Chromosome], size: int) -> None:
    pass


def age_tournament(items: List[Chromosome], size: int) -> None:
    pass
