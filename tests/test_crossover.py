from unittest import TestCase
from operators.crossover import *


class TestCrossover(TestCase):

    def test_single_point(self):
        a, b = single_point([1, 2], [3, 4])
        self.assertListEqual(a, [1, 4])
        self.assertListEqual(b, [3, 2])
