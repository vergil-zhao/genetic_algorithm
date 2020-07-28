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

import numpy as np

from random import random


def divcon_a(items: list, hi: float = 0.1, lo: float = 0.02, **kwargs) -> list:
    """
    Diversity Control Algorithm A
    Calculate distances between all items, set penalty to those who have
    many neighbors.

    :param items: is a list of chromosomes(list of genes) or fitness values
    :param hi: higher bound of distance threshold
    :param lo: higher bound of distance threshold
    :return: list of penalty
    """
    assert hi >= lo

    dist = [[0] * len(items) for _i in range(len(items))]
    for i in range(len(items) - 1):
        genes_i = np.array(items[i] if isinstance(items[i], list) else [items[i]])
        for j in range(i + 1, len(items)):
            genes_j = np.array(items[j] if isinstance(items[j], list) else [items[j]])
            dist[i][j] = np.linalg.norm(genes_j - genes_i)
            dist[j][i] = dist[i][j]

    alpha = lo + (random() * (hi - lo))
    threshold = np.mean(dist) * alpha

    penalties = []
    for i in range(len(items)):
        neighbors = len(list(filter(lambda x: x < threshold, dist[i])))
        penalties.append(1 / neighbors)

    return penalties


def divcon_b(items: list, hi: float = 2.0, lo: float = 0.5, trials: int = 3, **kwargs) -> list:
    """

    :param items: is a list of chromosomes(list of genes) or fitness values
    :param hi: higher bound of numbers of bin relative to size of items
    :param lo: lower bound of numbers of bin relative to size of items
    :param trials: number of trials
    :return:
    """
    rows, cols = np.shape(items)
    penalties = [0] * rows

    for _t in range(trials):
        bin_num = round((lo + random() * (hi - lo)) * rows)
        bins = np.linspace(0, 1, bin_num + 1)
        vector = np.random.permutation(cols)
        sums = vector.dot(np.array(items).transpose())

        groups = [[] for _i in range(bin_num)]
        for i, item in enumerate(sums):
            for j in reversed(range(bin_num)):
                if item >= bins[j]:
                    groups[j].append(i)
                    break

        for group in groups:
            for index in group:
                if len(group) > 0:
                    penalty = 1 / len(group)
                    if penalty > penalties[index]:
                        penalties[index] = penalty

    return [x if x > 0 else 1 for x in penalties]
