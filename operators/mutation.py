import random

from typing import List


def random_mutate(genes: List[float], rate: float, **kwargs) -> List[float]:
    """
    Randomly change a gene value by a fixed probability

    :param genes: list of gene
    :param rate: probablity of mutate for every gene value
    :return: mutated genes
    """
    offspring = genes[:]
    for i in range(len(offspring)):
        if rate > random.random():
            offspring[i] = random.random()
    return offspring


def norm_dist(genes: List[float], rate: float, sigma: float = 0.2, **kwargs) -> List[float]:
    """
    Randomly change a gene value by a normal distributed probability,
    center is the gene itself

    :param genes: list of gene
    :param rate: probablity of mutate for every gene value
    :param sigma: sigma for normal distribution
    :return: mutated genes
    """
    offspring = genes[:]

    for i in range(len(offspring)):
        if rate > random.random():
            offspring[i] += random.gauss(0, sigma)

    return offspring
