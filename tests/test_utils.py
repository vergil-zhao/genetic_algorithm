import unittest

from utils import *


class TestUtils(unittest.TestCase):

    def test_create_wheel(self):
        wheel = create_wheel([1, 2, 3, 4, 5])
        self.assertListEqual(wheel, [1, 3, 6, 10, 15])

    def test_pick_from_wheel(self):
        wheel = create_wheel([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        class A:
            def __init__(self):
                self.property_1 = 1
                self.property_2 = {'key': 10}

        items = [A() for _i in range(10)]

        pool = pick_from_wheel(items, wheel, 5)

        for i in range(10):
            for j in range(5):
                self.assertIsNot(items[i], pool[j])
                self.assertIsNot(items[i].property_2, pool[j].property_2)
