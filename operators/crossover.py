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

from typing import List


def single_point(a: List[float], b: List[float], **_) -> (List[float], List[float]):
    """
    Crossover genes at a random cut point, e.g.

    Cut point = 1
    a: 0.1 0.2 | 0.3 0.4 0.5
    b: 0.6 0.7 | 0.8 0.9 1.0

    Offsprings will be:
    0.6 0.7 0.3 0.4 0.5
    0.1 0.2 0.8 0.9 1.0

    :param a: list of genes
    :param b: list of genes
    :return: two offsprings
    """
    if len(a) != len(b):
        raise ValueError('chromosome length should be same')

    if len(a) <= 1:
        return a[:], b[:]

    point = random.randint(1, len(a) - 1)
    return (
        a[:point] + b[point:],
        b[:point] + a[point:]
    )


def blend(a: List[float], b: List[float], alpha=0.5, **_) -> (List[float], List[float]):
    """
    Blend gene numbers randomly within a range depended on parent genes

    :param a: list of genes
    :param b: list of genes
    :param alpha: range factor
    :return: two offsprings
    """
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


def sbx(a: List[float], b: List[float], eta=2, **_) -> (List[float], List[float]):
    """
    Simulated Binary Crossover

    In binary crossover
    when cut point = 3
    1001|0010 = 146
    0111|1001 = 121
    avg = 133.5
    offsprings:
    10011001 = 153
    01110010 = 114
    avg = 133.5

    This operator has the same attribute with Binary Crossover, the average value of parents genes equals
    the average value of offsprings genes at the same position like it shows above.

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
