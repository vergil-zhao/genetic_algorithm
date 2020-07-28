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

from operators.utils import tournament


def random_pick(items: list, size: int, **kwargs) -> None:
    """
    Randomly pick items and set to eliminated

    :param items: chromosomes
    :param size: number of elimination
    """
    pool = random.sample(items, size)
    for item in pool:
        item.is_alive = False


def fitness_tournament(items: list, size: int, **kwargs) -> None:
    """
    Tournament by fitness

    :param items: chromosomes
    :param size: number of elimination
    """
    pool = tournament(items, [-item.fitness for item in items], size)
    for item in pool:
        item.is_alive = False


def age_tournament(items: list, size: int, **kwargs) -> None:
    """
    Tournament by age

    :param items: chromosomes
    :param size: number of elimination
    """
    pool = tournament(items, [item.age for item in items], size)
    for item in pool:
        item.is_alive = False
