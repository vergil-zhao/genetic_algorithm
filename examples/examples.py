#  Copyright (C) 2020 All Rights Reserved
#
#      This file is part of genetic_algorithm.
#
#      Foobar is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Foobar is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#  Written by Vergil Choi <vergil.choi.zyc@gmail.com>, Jul 2020
#

import statistics
import math
import matplotlib.pyplot as plt

from ga.algorithms import GA
from ga.conf import FloatItem, Config
from operators.utils import print_name


def plot(gen, std, best, mean):
    def update(p: GA):
        values = [item.fitness for item in p.chromosomes]
        gen.append(p.generation)
        std.append(statistics.stdev(values))
        best.append(p.best().raw_fitness)
        mean.append(statistics.mean(values))
    return update


def plot_ga(title, gen, std, best, mean):
    fig, (std_gen, best_gen) = plt.subplots(2, 1, figsize=(5, 10), dpi=220)

    # std_gen.set_xlim(0, 100)
    # std_gen.set_ylim(0, 1)

    std_gen.plot(gen, std)
    std_gen.set_title(title)
    std_gen.set_xlabel('Number of Generation')
    std_gen.set_ylabel('Standard Deviation')

    best_gen.plot(gen, best, gen, mean)
    best_gen.set_xlabel('Number of Generation')
    best_gen.set_ylabel('Fitness Value')

    plt.show()


@print_name
def wave_func():
    def wave(x): return 5 * math.sin(3 * x) + ((x - 30) / 5) ** 2 + 10

    p = GA(Config(
        gene_pattern=[FloatItem(0, 100, 5)],
        fit=lambda data: 100 / wave(data[0]),
        size=20,
    ))

    gen = []
    std = []
    best = []
    mean = []
    p.evolve(plot(gen, std, best, mean))

    best_individual = p.best()
    best_ans = best_individual.decode()
    print(f'BEST:     {best_ans}\n'
          f'RESULT:   {wave(best_ans[0])}\n'
          f'FIT:      {best_individual.raw_fitness}'
          f'FIT MEAN: {mean[-1]}\n'
          f'FIT STD:  {std[-1]}\n')
    plot_ga('Min(Wave Function)', gen, std, best, mean)


@print_name
def rosenbrock_func():
    def rosenbrock(x, y): return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2

    p = GA(Config(
        gene_pattern=[FloatItem(-2, 2, 10), FloatItem(-1, 3, 10)],
        fit=lambda data: 1 / (rosenbrock(data[0], data[1]) + 0.001),
    ))

    gen = []
    std = []
    best = []
    mean = []
    p.evolve(plot(gen, std, best, mean))

    best_individual = p.best()
    best_ans = best_individual.decode()
    print(f'BEST:     {best_ans}\n'
          f'RESULT:   {rosenbrock(best_ans[0], best_ans[1])}\n'
          f'FIT:      {best_individual.raw_fitness}\n'
          f'FIT MEAN: {mean[-1]}\n'
          f'FIT STD:  {std[-1]}\n')
    plot_ga('Min(Rosenbrock Function)', gen, std, best, mean)


if __name__ == '__main__':
    rosenbrock_func()
