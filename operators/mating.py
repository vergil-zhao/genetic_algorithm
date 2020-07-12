import random

from typing import List


def _mate(chromosomes: List) -> List:
    offsprings = []
    for i in range(len(chromosomes) // 2):
        a, b = chromosomes[i * 2] + chromosomes[i * 2 + 1]
        offsprings.append(a)
        offsprings.append(b)

    if len(chromosomes) % 2 != 0:
        a, b = chromosomes[-1] + random.choice(chromosomes)
        if random.random() < 0.5:
            offsprings.append(a)
        else:
            offsprings.append(b)

    return offsprings


def random_mating(chromosomes: List) -> List:
    """
    Randomly pick two chromosomes as parents, chromosome can be picked many times

    :param chromosomes: parents
    :return: offsprings
    """
    offsprings = []
    for i in range(len(chromosomes)):
        parents = random.choices(chromosomes, k=2)
        a, b = parents[0] + parents[1]
        offsprings.append(a)
        offsprings.append(b)

    return offsprings


def random_mating_once(chromosomes: List) -> List:
    """
    Randomly pick two chromosomes as parents, every chromosome can only be picked once

    :param chromosomes: parents
    :return: offsprings
    """
    pool = chromosomes[:]
    random.shuffle(pool)
    return _mate(pool)


def phenotypic_mating(chromosomes: List) -> List:
    """
    Pick parents ordered by fitness,
    chromosomes whose fitness close to each other will mate

    :param chromosomes: parents
    :return: offsprings
    """
    pool = sorted(chromosomes)
    return _mate(pool)


def genotypic_mating(chromosomes: List) -> List:
    """
    TODO: Pick parents ordered by gene similarity,
    chromosomes whose gene close to each other will mate

    :param chromosomes: parents
    :return: offsprings
    """
    pass
