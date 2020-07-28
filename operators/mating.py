#  Copyright (C) 2020 All Rights Reserved
#
#      This file is part of genetic_algorithm.
#
#      Foobar is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Foobar is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#  Written by Vergil Choi <vergil.choi.zyc@gmail.com>, Jul 2020
#

import random


def _mate(chromosomes: list) -> list:
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


def random_mating(chromosomes: list) -> list:
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


def random_mating_once(chromosomes: list) -> list:
    """
    Randomly pick two chromosomes as parents, every chromosome can only be picked once

    :param chromosomes: parents
    :return: offsprings
    """
    pool = chromosomes[:]
    random.shuffle(pool)
    return _mate(pool)


def phenotypic_mating(chromosomes: list) -> list:
    """
    Pick parents ordered by fitness,
    chromosomes whose fitness close to each other will mate

    :param chromosomes: parents
    :return: offsprings
    """
    pool = sorted(chromosomes)
    return _mate(pool)


def genotypic_mating(chromosomes: list) -> list:
    """
    TODO: Pick parents ordered by gene similarity,
    chromosomes whose gene close to each other will mate

    :param chromosomes: parents
    :return: offsprings
    """
    pass
