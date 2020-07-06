import unittest
import statistics
import math
import matplotlib.pyplot as plt

from ga.population import Population
from ga.conf import FloatItem, Config
from operators.utils import print_name


def plot(gen, std, best, mean):
    def update(p: Population):
        values = [item.fitness for item in p.chromosomes]
        gen.append(p.generations)
        std.append(statistics.stdev(values))
        best.append(max(p.chromosomes).fitness)
        mean.append(statistics.mean(values))

    return update


def plot_ga(gen, std, best, mean):
    fig, (std_gen, best_gen) = plt.subplots(2, 1, figsize=(5, 10), dpi=220)
    # std_gen.set_xlim(0, 100)
    # std_gen.set_ylim(0, 1)
    std_gen.plot(gen, std)
    best_gen.plot(gen, best, gen, mean)
    plt.show()


class TestMain(unittest.TestCase):

    @print_name
    def test_wave_func(self):
        def wave(x): return 5 * math.sin(3 * x) + ((x - 30) / 5) ** 2 + 10

        def wave_fit(data):
            self.assertGreaterEqual(data[0], 0)
            self.assertLessEqual(data[0], 100)
            return 100 / wave(data[0])

        p = Population(Config(
            gene_pattern=[FloatItem(0, 100, 3)],
            fit=wave_fit,
            size=11,
            max_gen=500
        ))

        gen = []
        std = []
        best = []
        mean = []
        p.evolve(plot(gen, std, best, mean))
        best_ans = max(p.chromosomes)
        print(f'BEST: {best_ans} VALUE: {wave(best_ans[0])}')
        print(p)
        plot_ga(gen, std, best, mean)

    @print_name
    def test_rosenbrock_func(self):
        def rosenbrock(x, y): return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2

        def rosenbrock_fit(data):
            self.assertGreaterEqual(data[0], -2)
            self.assertLessEqual(data[0], 2)
            self.assertGreaterEqual(data[1], -1)
            self.assertLessEqual(data[1], 3)
            return 1 / (rosenbrock(data[0], data[1]) + 0.001)

        p = Population(Config(
            gene_pattern=[FloatItem(-2, 2, 8), FloatItem(-1, 3, 8)],
            fit=rosenbrock_fit,
            size=11,
            max_gen=500
        ))

        gen = []
        std = []
        best = []
        mean = []
        p.evolve(plot(gen, std, best, mean))
        best_ans = max(p.chromosomes)
        print(f'BEST: {best_ans} VALUE: {rosenbrock(best_ans[0], best_ans[1])}')
        print(p)
        plot_ga(gen, std, best, mean)
