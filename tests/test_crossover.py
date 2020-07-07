import operators.crossover as crs

from unittest import TestCase


class TestCrossover(TestCase):

    def test_single_point(self):
        a, b = crs.single_point([1, 2], [3, 4])
        self.assertListEqual(a, [1, 4])
        self.assertListEqual(b, [3, 2])

    def test_blend(self):
        a, b = crs.blend([0.3, 0.5], [0.4, 0.6])
        self.assertTrue(0.25 <= a[0] <= 0.45)
        self.assertTrue(0.45 <= a[1] <= 0.65)
        self.assertTrue(0.25 <= b[0] <= 0.45)
        self.assertTrue(0.45 <= b[1] <= 0.65)
        print(a, b)

    def test_simulated_binary(self):
        a, b = crs.sbx([0, 0.6], [1, 0.4])
        self.assertAlmostEqual(a[0] + b[0], 1)
        self.assertAlmostEqual(a[1] + b[1], 1)
        print(a, b)
