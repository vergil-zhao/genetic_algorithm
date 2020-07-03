import matplotlib.pyplot as plt
import statistics
import math

from population import Population, FloatItem
from utils import prettify_matrix


def seperated_tests():
    p = Population(
        gene_pattern=[FloatItem(1, 5, 3), FloatItem(2, 3, 3), FloatItem(0, 1, 2), FloatItem(1, 10, 5)],
        fit=sum
    )
    p.evaluate(p.chromosomes)

    print('======= Original Population =======')
    print(p)

    p.crossover()
    print('======= Crossover Offspring =======')
    print(prettify_matrix(p.offsprings))

    p.mutate()
    print('======== Mutated Offsping =========')
    print(prettify_matrix(p.offsprings))

    p.evaluate(p.offsprings)
    print('======== Offsping Fitnesses =======')
    for ch in p.offsprings:
        print(ch.fitness)

    p.eliminate()
    print('======== Eliminate Parents ========')
    for ch in p.chromosomes:
        print(f'{ch.fitness} - {ch.is_alive}')

    p.replace()
    print('======== Replaced Poplation =======')
    for ch in p.chromosomes:
        print(f'{ch.fitness} - {ch.is_alive}')


def plot(gen, std, best, mean):
    def update(p: Population):
        values = [item.fitness for item in p.chromosomes]
        gen.append(p.generations)
        std.append(statistics.stdev(values))
        best.append(max(p.chromosomes).fitness)
        mean.append(statistics.mean(values))

    return update


def test():
    def rosenbrock(x, y): return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2
    def wave(x): return 5 * math.sin(3 * x) + ((x - 30) / 5) ** 2 + 10

    p = Population(
        gene_pattern=[FloatItem(-2, 2, 8), FloatItem(-1, 3, 8)],
        # gene_pattern=[FloatItem(0, 100, 3)],
        fit=lambda x: 1 / (rosenbrock(x[0], x[1]) + 0.001),
        # fit=lambda x: 100 / wave(x[0]),
        size=11,
        max_gen=500
    )

    fig, (std_gen, best_gen) = plt.subplots(2, 1, figsize=(5, 10), dpi=220)
    gen = []
    std = []
    best = []
    mean = []
    # std_gen.set_xlim(0, 100)
    # std_gen.set_ylim(0, 1)

    p.evolve(plot(gen, std, best, mean))
    best_ans = max(p.chromosomes)
    print(f'BEST: {best_ans} VALUE: {wave(best_ans[0])}')
    print(p)

    std_gen.plot(gen, std)
    best_gen.plot(gen, best, gen, mean)
    plt.show()


if __name__ == '__main__':
    test()