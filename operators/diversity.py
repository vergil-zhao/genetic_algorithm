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

from numpy import array, mean
from numpy.linalg import norm
from random import random


def divcon_a(items: list, hi: float = 0.1, lo: float = 0.02):
    """
    Diversity Control Algorithm A
    Calculate distances between all items, set penalty to those who have
    many neighbors.

    :param items: is a list of chromosomes(list of genes) or fitness values
    :param hi: higher bound of distance threshold
    :param lo: higher bound of distance threshold
    :return:
    """
    assert hi >= lo

    dist = [[0] * len(items) for _i in range(len(items))]
    for i in range(len(items) - 1):
        genes_i = array(items[i] if isinstance(items[i], list) else [items[i]])
        for j in range(i + 1, len(items)):
            genes_j = array(items[j] if isinstance(items[j], list) else [items[j]])
            dist[i][j] = norm(genes_j - genes_i)
            dist[j][i] = dist[i][j]

    alpha = lo + (random() * (hi - lo))
    threshold = mean(dist) * alpha

    penalties = []
    for i in range(len(items)):
        neighbors = len(list(filter(lambda x: x < threshold, dist[i])))
        penalties.append(1 / neighbors)

    return penalties
