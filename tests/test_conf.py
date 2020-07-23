from ga.conf import Config, FloatItem

from unittest import TestCase


class TestCrossover(TestCase):

    config_map = {
        'pattern': [
            {
                'start': 1,
                'end': 5,
                'precision': 5,
            },
            {
                'start': 2,
                'end': 7,
                'precision': 6,
            },
            {
                'start': 3,
                'end': 9,
                'precision': 7,
            },
        ],
        'size': 10,
        'crossoverRate': 0.5,
        'mutationRate': 0.01,
        'elitism': True,
        'maxGen': 10,
    }

    def test_from_dict(self):
        config = Config.from_dict(self.config_map)
        self.assertDictEqual(config.serialize(), self.config_map)

    def test_serilize(self):
        config = Config(
            [FloatItem(1, 5, 5), FloatItem(2, 7, 6), FloatItem(3, 9, 7)],
            size=10,
            crossover_rate=0.5,
            mutation_rate=0.01,
            elitism=True,
            max_gen=10,
        )
        self.assertDictEqual(config.serialize(), self.config_map)
