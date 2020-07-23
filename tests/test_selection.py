import unittest
import operators.selection as slc

from ga.genetic import Chromosome
from ga.conf import Config, FloatItem


class TestSelection(unittest.TestCase):
    def setUp(self) -> None:
        pattern = [
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5)
        ]

        self.chromosomes = [Chromosome(Config(pattern, sum)) for _i in range(10)]

        for i in range(10):
            self.chromosomes[i].fitness = i

    # @print_name
    def test_random_pick(self):
        p = slc.random_pick(self.chromosomes, 5)
        self.assertEqual(len(p), 5)

    # @print_name
    def test_roulette_wheel(self):
        p = slc.roulette_wheel(self.chromosomes, 5)
        self.assertEqual(len(p), 5)

    # @print_name
    def test_fitness_tournament(self):
        p = slc.fitness_tournament(self.chromosomes, 5)
        self.assertEqual(len(p), 5)

    # @print_name
    def test_rank(self):
        p = slc.rank(self.chromosomes, 5)
        self.assertEqual(len(p), 5)
