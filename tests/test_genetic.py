import unittest

from ga.conf import FloatItem, Config
from ga.genetic import Chromosome


class TestGenetic(unittest.TestCase):

    def setUp(self) -> None:
        pattern = [
            FloatItem(0, 1, 5),
            FloatItem(-1, 0, 5),
            FloatItem(-100, 100, 5),
        ]

        self.config = Config(
            pattern,
            fit=sum,
        )

        self.chromosome = Chromosome(self.config)

    def test_generate(self):
        self.assertGreaterEqual(self.chromosome.genes, [0, 0, 0])
        self.assertLessEqual(self.chromosome.genes, [1, 1, 1])

    def test_mutate(self):
        self.chromosome.mutate()
        self.assertGreaterEqual(self.chromosome.genes, [0, 0, 0])
        self.assertLessEqual(self.chromosome.genes, [1, 1, 1])

    def test_decode(self):
        c = Chromosome(self.config, [0, 0, 0])
        self.assertEqual(c.decode(), [0, -1, -100])

        c = Chromosome(self.config, [0.5, 0.5, 0.5])
        self.assertEqual(c.decode(), [0.5, -0.5, 0])

    def test_crossover(self):
        c = Chromosome(self.config, [0, 0, 0])
        a, b = self.chromosome + c
        self.assertEqual(a.config, self.chromosome.config)
        self.assertEqual(b.config, self.chromosome.config)

        self.assertEqual(len(a.genes), len(self.chromosome.genes))
        self.assertEqual(len(b.genes), len(self.chromosome.genes))

    def test_update(self):
        c = Chromosome(self.config)
        c.update({
            'parameters': [0.0, -1.0, -100.0],
            'fitness': 1.0,
            'alive': True,
            'age': 0,
        })
        self.assertListEqual(c.genes, [0.0, 0.0, 0.0])
        self.assertListEqual(c.decode(), [0.0, -1.0, -100.0])

        c.update({
            'parameters': [0.5, -0.5, 0],
            'fitness': 2.0,
            'alive': True,
            'age': 0,
        })
        self.assertListEqual(c.genes, [0.5, 0.5, 0.5])
        self.assertListEqual(c.decode(), [0.5, -0.5, 0])

    def test_serialize(self):
        c = Chromosome(self.config, [0, 0, 0])
        self.assertDictEqual(c.serialize(), {
            'parameters': [0.0, -1.0, -100.0],
            'fitness': 0.0,
            'alive': True,
            'age': 0,
        })
