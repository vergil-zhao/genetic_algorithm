import unittest

from ga.conf import Config, FloatItem
from ga.genetic import Chromosome
from ga.population import Population


class TestPopulation(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(
            gene_pattern=[FloatItem(0, 1, 5), FloatItem(0, 5, 5), FloatItem(-5, 5, 5)],
            fit=sum,
            size=12,
            max_gen=100,
            elitism=1
        )
        self.chromosomes = [
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
            Chromosome(self.config, [0, 0, 0]),
        ]

    def test_generate(self):
        p = Population(self.config, self.chromosomes)
        self.assertEqual(len(p.chromosomes), 12)
        self.assertEqual(p.generations, 0)

    def test_selection(self):
        p = Population(self.config, self.chromosomes)
        self.assertEqual(len(p.create_mating_pool()), 9)

    def test_age_grow(self):
        p = Population(self.config, self.chromosomes)
        p.age_grow()
        for item in p.chromosomes:
            self.assertEqual(item.age, 1)

    def test_eliminate(self):
        p = Population(self.config, self.chromosomes)
        p.eliminate()
        count = 0
        for item in p.chromosomes:
            if not item.is_alive:
                count += 1
        self.assertEqual(count, 9)

    def test_crossover(self):
        p = Population(self.config, self.chromosomes)
        p.crossover()
        self.assertEqual(len(p.offsprings), 9)

    def test_evaluate(self):
        p = Population(self.config, self.chromosomes)
        p.evaluate(p.chromosomes)
        for item in p.chromosomes:
            self.assertEqual(item.fitness, sum(item.decode()))

    def test_replace(self):
        p = Population(self.config, self.chromosomes)
        p.evaluate(p.chromosomes)
        p.crossover()
        p.mutate()
        p.evaluate(p.offsprings)
        p.eliminate()

        origin = p.chromosomes[:]
        p.replace()
        self.assertNotEqual(origin, p.chromosomes)
