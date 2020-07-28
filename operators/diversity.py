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
#  Reference:
#  https://engineering.purdue.edu/~sudhoff/Software%20Distribution/GOSET%202.3%20manual.pdf
#

import numpy as np

from random import random, randrange


def _array(item):
    return np.array(item if isinstance(item, list) else [item])


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

    # calculate Euclidean distance between all items
    dist = np.zeros((len(items), len(items)))
    for i in range(len(items) - 1):
        genes_i = _array(items[i])
        for j in range(i + 1, len(items)):
            genes_j = _array(items[j])
            dist[i][j] = np.linalg.norm(genes_j - genes_i)
            dist[j][i] = dist[i][j]

    # calculate threshold
    alpha = lo + (random() * (hi - lo))
    threshold = np.mean(dist) * alpha

    # calculate penalty
    penalties = []
    for i in range(len(items)):
        neighbors = len(list(filter(lambda x: x < threshold, dist[i])))
        penalties.append(1 / neighbors)

    return penalties


def divcon_b(items: list, hi: float = 2.0, lo: float = 0.5, trials: int = 3, **kwargs) -> list:
    """
    Diversity Control Algorithm B
    Calculate weighted sum for all items with a randomly generated weight
    vector. Then the sums will be hashed to bins. Penalty values depend on the
    number of items in the same bin.

    :param items: is a list of chromosomes(list of genes) or fitness values
    :param hi: higher bound of numbers of bin relative to size of items
    :param lo: lower bound of numbers of bin relative to size of items
    :param trials: number of trials
    :return: list of penalty
    """
    assert hi >= lo
    assert isinstance(trials, int) and trials > 0

    rows, cols = np.shape(items)
    penalties = [0] * rows

    for _t in range(trials):
        # create bins
        bin_num = round((lo + random() * (hi - lo)) * rows)
        bins = np.linspace(0, 1, bin_num + 1)

        # random vector
        vector = np.random.permutation(cols)

        # multiply and hash
        sums = vector.dot(np.array(items).transpose())
        sums = [i % 1 for i in sums]

        # allocate bins
        groups = [[] for _i in range(bin_num)]
        for i, item in enumerate(sums):
            for j in reversed(range(bin_num)):
                if item >= bins[j]:
                    groups[j].append(i)
                    break

        # keep bigger value to prevent special weight
        # which cause different items have similar sum
        for group in groups:
            for index in group:
                penalty = 1 / len(group) if len(group) > 0 else 1
                if penalty > penalties[index]:
                    penalties[index] = penalty

    return penalties


def divcon_c(items: list, dist_const: float = 0.001, **kwargs) -> list:
    """
    Diversity Control Algorithm C
    Penalty depends on calculating the infinity norm between all items.

    :param items: is a list of chromosomes(list of genes) or fitness values
    :param dist_const: distance constant, the bigger value the more severe penalty
    :return: list of penalty
    """
    assert dist_const > 0

    # calculate infinity norm between all items
    dist = np.zeros((len(items), len(items)))
    for i in range(len(items) - 1):
        genes_i = _array(items[i])
        for j in range(i + 1, len(items)):
            genes_j = _array(items[j])
            dist[i][j] = np.linalg.norm(genes_j - genes_i, np.inf)
            dist[j][i] = dist[i][j]

    # calculate penalty
    penalties = []
    for i in range(len(items)):
        penalties.append(1 / np.sum(np.exp(- dist[i] / dist_const)))

    return penalties


def divcon_d(items: list, dist_const: float = 0.001, sample: int = 3, **kwargs) -> list:
    """
    Diversity Control Algorithm D
    Similar to C. Only choose a subset of entire list to calculate infinity norm.

    :param items: is a list of chromosomes(list of genes) or fitness values
    :param dist_const: distance constant, the bigger value the more severe penalty
    :param sample: number of items to be compared with
    :return: list of penalty
    """
    assert dist_const > 0
    assert sample > 0
    assert len(items) > sample

    # Calculate infinity norm between a subset of entire items
    dist = np.zeros((len(items), sample))
    for i in range(len(items)):
        genes_i = _array(items[i])
        for j in range(sample):
            while True:
                index = randrange(len(items))
                if index == i:
                    continue
                genes_j = _array(items[index])
                dist[i][j] = np.linalg.norm(genes_j - genes_i, np.inf)
                break

    # calculate penalty
    penalties = []
    for i in range(len(items)):
        penalties.append(1 / (1 + len(items) / sample * np.sum(np.exp(- dist[i] / dist_const))))

    return penalties
