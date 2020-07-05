import operators.crossover as crs

from unittest import TestCase


class TestCrossover(TestCase):

    def test_single_point(self):
        a, b = crs.single_point([1, 2], [3, 4])
        self.assertListEqual(a, [1, 4])
        self.assertListEqual(b, [3, 2])
