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

from operators.utils import create_wheel, pick_from_wheel, tournament


def random_pick(items: list, size: int, **kwargs) -> list:
    """
    Randomly pick items to create a pool.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    return random.sample(items, size)


def roulette_wheel(items: list, size: int, **kwargs) -> list:
    """
    Pick item randomly at a roulette wheel of which width is the fitness value.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    wheel = create_wheel([item.fitness for item in items])
    return pick_from_wheel(items, wheel, size)


def fitness_tournament(items: list, size: int, **kwargs) -> list:
    """
    Pick item by rounds of tournament.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    return tournament(items, [item.fitness for item in items], size)


def rank(items: list, size: int, **kwargs) -> list:
    """
    Derived from roulette wheel, roulette created by rank number,
    the higher fitness value the rank number will be.

    :param items: list of chromosome, fitness value has to be positive
    :param size: the mating mating pool
    :return: the mating pool
    """
    items_sorted = sorted(items)
    length = len(items_sorted)

    wheel = create_wheel([i for i in range(1, length + 1)])
    return pick_from_wheel(items, wheel, size)
