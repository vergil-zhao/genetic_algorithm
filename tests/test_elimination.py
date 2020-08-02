from unittest import TestCase

import operators.elimination as elm
from ga.conf import Config, FloatItem
from ga.genetic import Chromosome


class TestElimination(TestCase):
    def setUp(self) -> None:
        pattern = [
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5)
        ]

        self.chromosomes = [Chromosome(Config(pattern, sum)) for _i in range(10)]

        for i, c in enumerate(self.chromosomes):
            c.age = i
            c.fitness = i

    def test_random_pick(self):
        elm.random_pick(self.chromosomes, 5)

        count = 0
        for item in self.chromosomes:
            if not item.is_alive:
                count += 1

        self.assertEqual(count, 5)

    # @print_name
    def test_fitness_tournament(self):
        elm.fitness_tournament(self.chromosomes, 5)

        count = 0
        for item in self.chromosomes:
            if not item.is_alive:
                count += 1

        self.assertEqual(count, 5)
        # print([item.fitness for item in self.chromosomes if item.is_alive])

    # @print_name
    def test_age_tournament(self):
        elm.age_tournament(self.chromosomes, 5)

        count = 0
        for item in self.chromosomes:
            if not item.is_alive:
                count += 1

        self.assertEqual(count, 5)
        # print([item.age for item in self.chromosomes if item.is_alive])
