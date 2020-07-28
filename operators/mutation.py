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
