import unittest

from operators.selection import *
from genetic import Chromosome, FloatItem


def test(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        func(*args, **kwargs)
    return wrapper


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

    @test
    def test_random_pick(self):
        print([c.fitness for c in random_pick(self.chromosomes, 5)])

    @test
    def test_roulette_wheel(self):
        print([c.fitness for c in roulette_wheel(self.chromosomes, 5)])

    @test
    def test_tournament(self):
        print([c.fitness for c in tournament(self.chromosomes, 5)])

    @test
    def test_rank(self):
        print([c.fitness for c in rank(self.chromosomes, 5)])
