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

from unittest import TestCase
from operators.scaling import *


class TestScaling(TestCase):

    case = [1, 2, 3, 4, 5]

    def test_offset(self):
        func = offset(self.case)
        self.assertEqual(func(1), 0)
        self.assertEqual(func(5), 4)

    def test_linear_avg(self):
        a = 13.5
        b = -37.5
        func = linear_avg(self.case)
        self.assertEqual(func(1), a + b)
        self.assertEqual(func(5), 30)

    def test_linear_med(self):
        a = 13.5
        b = -37.5
        func = linear_avg(self.case)
        self.assertEqual(func(1), a + b)
        self.assertEqual(func(5), 30)

    def test_linear_map(self):
        func = linear_map(self.case)
        self.assertEqual(func(1), 1)
        self.assertEqual(func(5), 10)

    def test_truncate(self):
        func = truncate(self.case, 0)
        self.assertEqual(func(1), -2)
        self.assertEqual(func(5), 2)

    def test_quadratic(self):
        func = quadratic(self.case)
        self.assertAlmostEqual(func(1), 0.01)
        self.assertAlmostEqual(func(5), 10)
        self.assertAlmostEqual(func(3), 1)
