import unittest
import operators.selection as slc

from genetic import Chromosome, FloatItem
from utils import print_name


class TestSelection(unittest.TestCase):
    def setUp(self) -> None:
        pattern = [
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5)
        ]

        self.chromosomes = [Chromosome(pattern=pattern) for _i in range(10)]

        for i in range(10):
            self.chromosomes[i].fitness = i

    @print_name
    def test_random_pick(self):
        print([c.fitness for c in slc.random_pick(self.chromosomes, 5)])

    @print_name
    def test_roulette_wheel(self):
        print([c.fitness for c in slc.roulette_wheel(self.chromosomes, 5)])

    @print_name
    def test_fitness_tournament(self):
        print([c.fitness for c in slc.fitness_tournament(self.chromosomes, 5)])

    @print_name
    def test_rank(self):
        print([c.fitness for c in slc.rank(self.chromosomes, 5)])
