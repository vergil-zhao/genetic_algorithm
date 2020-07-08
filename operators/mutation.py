import random

from typing import List


def random_mutate(genes: List[float], rate: float) -> List[float]:
    offspring = genes[:]
    for i in range(len(offspring)):
        if rate > random.random():
            offspring[i] = random.random()
    return offspring


def norm_dist(genes: List[float], rate: float, sigma: float = 0.2) -> List[float]:
    offspring = genes[:]

    for i in range(len(offspring)):
        if rate > random.random():
            offspring[i] += random.gauss(0, sigma)

    return offspring
