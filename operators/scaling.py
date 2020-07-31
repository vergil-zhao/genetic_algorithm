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

from typing import List, Callable


def offset(items: List[float], **kwargs) -> Callable[[float], float]:
    """
    Move down all items by a min(items)

    :param items: fitness values
    :return: mapping function
    """
    b = min(items)
    return lambda x: x - b


def linear_avg(items: List[float], k: float = 10.0, **kwargs) -> Callable[[float], float]:
    """
    Keep average(items) unchanged, scale up items greater then avg,
    scale down items lesser then avg.

    :param items: fitness values
    :param k: scale factor
    :return: mapping function
    """
    assert k >= 1

    avg = np.average(items)
    a = (k - 1) * avg / (max(items) - avg)
    b = avg * (1 - a)
    return lambda x: a * x + b


def linear_med(items: List[float], k: float = 10.0, **kwargs) -> Callable[[float], float]:
    """
    Keep median(items) unchanged, scale up items greater then med,
    scale down items lesser then med.

    :param items: fitness values
    :param k: scale factor
    :return: mapping function
    """
    assert k >= 1

    med = np.median(items)
    a = (k - 1) * med / (max(items) - med)
    b = med * (1 - a)
    return lambda x: a * x + b


def linear_map(items: List[float], k: float = 10.0, **kwargs) -> Callable[[float], float]:
    """
    A linear scaling maps min(items) to 1, maps max(items) to k.

    :param items: fitness values
    :param k: scale factor
    :return: mapping function
    """
    assert k >= 1

    m = min(items)
    a = (k - 1) / (max(items) - m)
    b = 1 - a * m
    return lambda x: a * x + b


def truncate(items: List[float], factor: float = 2.0, **kwargs) -> Callable[[float], float]:
    """
    Truncate lower part of items which smaller(greater) than average.

    :param items: fitness values
    :param factor: offset factor depending on standard deviation
                   indicates how far from average.
                   If positive, cut point is below the average, otherwise
                   above the average.
    :return: mapping function
    """
    std = np.std(items)
    avg = np.average(items)
    b = avg - factor * std
    return lambda x: x - b


def quadratic(items: List[float], hi: float = 10.0, lo: float = 0.01, **kwargs) -> Callable[[float], float]:
    """
    Non-linear mapping. Map min(items) to lo, max(items) to hi, average(items) to 1.
    The function is quadratic.

    :param items:
    :param hi:
    :param lo:
    :param kwargs:
    :return:
    """
    f_max = max(items)
    f_avg = np.average(items)
    f_min = min(items)

    left = np.linalg.inv(np.array([[f_max * f_max, f_max, 1],
                                   [f_avg * f_avg, f_avg, 1],
                                   [f_min * f_min, f_min, 1]]))
    right = np.array([hi, 1, lo]).transpose()

    params = list((left.dot(right)).transpose())

    return lambda x: params[0] * x * x + params[1] * x + params[2]
