import unittest

from ga.conf import Config, FloatItem
from ga.genetic import Chromosome
from ga.algorithms import GA, GAPassive


class TestGA(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(
            gene_pattern=[FloatItem(0, 1, 5), FloatItem(0, 5, 5), FloatItem(-5, 5, 5)],
            fit=lambda x: abs(sum(x)),
            size=12,
            max_gen=100,
            elitism=True
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
        p = GA(self.config, self.chromosomes)
        self.assertEqual(len(p.chromosomes), 12)
        self.assertEqual(p.generation, 0)

    def test_selection(self):
        p = GA(self.config, self.chromosomes)
        self.assertEqual(len(p.create_mating_pool()), 8)

    def test_age_grow(self):
        p = GA(self.config, self.chromosomes)
        p.age_grow()
        for item in p.chromosomes:
            self.assertEqual(item.age, 1)

    def test_eliminate(self):
        p = GA(self.config, self.chromosomes)
        p.eliminate()
        count = 0
        for item in p.chromosomes:
            if not item.is_alive:
                count += 1
        self.assertEqual(count, 8)

    def test_crossover(self):
        p = GA(self.config, self.chromosomes)
        p.crossover()
        self.assertEqual(len(p.offsprings), 8)

    def test_evaluate(self):
        p = GA(self.config, self.chromosomes)
        p.evaluate(p.chromosomes)
        for item in p.chromosomes:
            self.assertEqual(item.fitness, abs(sum(item.decode())))

    def test_replace(self):
        p = GA(self.config, self.chromosomes)
        p.evaluate(p.chromosomes)
        p.crossover()
        p.mutate()
        p.evaluate(p.offsprings)
        p.eliminate()

        origin = p.chromosomes[:]
        p.replace()
        self.assertNotEqual(origin, p.chromosomes)

    def test_serialize(self):
        p = GAPassive(
            self.config,
            0,
            self.chromosomes,
            None,
        )
        self.maxDiff = None
        self.assertDictEqual(p.serialize(), {
            'population': [{
                'parameters': [0.0, 0.0, -5.0],
                'fitness': 0.0,
                'alive': True,
                'age': 0,
            } for _i in range(len(self.chromosomes))],
            'offsprings': [],
            'generation': 0,
            'satisfied': False,
            'best': {
                'parameters': [0.0, 0.0, -5.0],
                'fitness': 0.0,
                'alive': True,
                'age': 0,
            }
        })
