import unittest
from operators import utils


class A:
    def __init__(self, i=0):
        self.property_1 = i
        self.property_2 = {'key': 10}

    def __repr__(self):
        return f'<A property_1={self.property_1}>'


class TestUtils(unittest.TestCase):

    def test_create_wheel(self):
        wheel = utils.create_wheel([1, 2, 3, 4, 5])
        self.assertListEqual(wheel, [1, 3, 6, 10, 15])

    def test_pick_from_wheel(self):
        wheel = utils.create_wheel([0, 0, 0, 0, 0, 10, 0, 0, 0, 0])

        items = [A(i) for i in range(10)]

        pool = utils.pick_from_wheel(items, wheel, 5)

        for i in range(10):
            for j in range(5):
                self.assertIsNot(items[i], pool[j])
                self.assertIsNot(items[i].property_2, pool[j].property_2)

        for item in pool:
            self.assertEqual(item.property_1, 5)

    def test_tournament(self):
        items = [A(i) for i in range(10)]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for _i in range(100):
            pool = utils.tournament(items, values, 5)
            count = 0
            for item in pool:
                for origin in items:
                    if item is origin:
                        count += 1
            self.assertEqual(count, 5)
            pool.sort(key=lambda a: a.property_1)
            for i in range(5):
                self.assertNotEqual(pool[i].property_1, pool[i - 1].property_1)

    def test_repair(self):
        genes = [-0.1, 1.1, -1.2, 2.2]
        repaired = utils.repair(genes)
        expected = [0.9, 0.1, 0.8, 0.2]
        self.assertEqual(len(genes), len(repaired))
        for i in range(len(repaired)):
            self.assertAlmostEqual(repaired[i], expected[i])

