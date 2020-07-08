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
    offsprings = []
    for i in range(len(chromosomes)):
        parents = random.choices(chromosomes, k=2)
        a, b = parents[0] + parents[1]
        offsprings.append(a)
        offsprings.append(b)

    return offsprings


def random_mating_once(chromosomes: List) -> List:
    pool = chromosomes[:]
    random.shuffle(pool)
    return _mate(pool)


def phenotypic_mating(chromosomes: List) -> List:
    pool = sorted(chromosomes)
    return _mate(pool)


def genotypic_mating(chromosomes: List) -> List:
    pass
