import random

from unittest import TestCase
from genetic import Chromosome, FloatItem
from operators.elimination import *


class TestElimination(TestCase):
    def setUp(self) -> None:
        pattern = [
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5),
            FloatItem(0, 10, 5)
        ]

        self.chromosomes = [Chromosome(pattern=pattern) for _i in range(10)]

        for c in self.chromosomes:
            c.age = random.randint(0, 100)
            c.fitness = random.randint(0, 100)

    def test_random_pick(self):
        random_pick(self.chromosomes, 5)

        count = 0
        for item in self.chromosomes:
            if not item.is_alive:
                count += 1

        self.assertEqual(count, 5)

    def test_fitness_tournament(self):
        fitness_tournament(self.chromosomes, 5)

        count = 0
        for item in self.chromosomes:
            if not item.is_alive:
                count += 1

        self.assertEqual(count, 5)
        print([item.fitness for item in self.chromosomes])

    def test_age_tournament(self):
        age_tournament(self.chromosomes, 5)

        count = 0
        for item in self.chromosomes:
            if not item.is_alive:
                count += 1

        self.assertEqual(count, 5)
        print([item.age for item in self.chromosomes])
