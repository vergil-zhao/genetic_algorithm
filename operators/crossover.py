import random

from typing import List


def single_point(a: List[float], b: List[float], **kwargs) -> (List[float], List[float]):
    if len(a) != len(b):
        raise ValueError('chromosome length should be same')

    if len(a) <= 1:
        return a[:], b[:]

    point = random.randint(1, len(a) - 1)
    return (
        a[:point] + b[point:],
        b[:point] + a[point:]
    )


def blend(a: List[float], b: List[float], alpha=0.5, **kwargs) -> (List[float], List[float]):
    if len(a) != len(b):
        raise ValueError('chromosome length should be same')

    offspring_1 = []
    offspring_2 = []
    for i in range(len(a)):
        low = min(a[i], b[i])
        hi = max(a[i], b[i])
        delta = alpha * (hi - low)
        offspring_1.append(random.uniform(low - delta, hi + delta))
        offspring_2.append(random.uniform(low - delta, hi + delta))

    return offspring_1, offspring_2


def sbx(a: List[float], b: List[float], eta=2, **kwargs) -> (List[float], List[float]):
    """
    Simulated Binary Crossover
    :param a: list of genes
    :param b: list of genes
    :param eta: distribution index, small value make the children far from the parents
    :return: two offsprings
    """
    if len(a) != len(b):
        raise ValueError('chromosome length should be same')

    offspring_1 = []
    offspring_2 = []
    for i in range(len(a)):
        mu = random.random()
        if mu <= 0.5:
            beta = pow(2 * mu, 1 / (eta + 1))
        else:
            beta = pow(1 / (2 * (1 - mu)), 1 / (eta + 1))

        offspring_1.append(0.5 * ((1 + beta) * a[i] + (1 - beta) * b[i]))
        offspring_2.append(0.5 * ((1 - beta) * a[i] + (1 + beta) * b[i]))

    return offspring_1, offspring_2

