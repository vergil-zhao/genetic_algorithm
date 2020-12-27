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

import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

from examples.functions import sphere, rosenbrock, rastrigin
from ga.algorithms import GA
from ga.conf import FloatItem, Config


class GAPlot:
    def __init__(
            self,
            n=2,
            gen=100,
            fit=None,
            title='GA Result Plot',
            noplot=False,
            save=False,
    ):
        self.gen = []
        self.best = []
        self.mean = []
        self.n = n
        self.grid = plt.GridSpec(2, 2)
        self.fit = fit
        self.title = title
        self.noplot = noplot
        self.save = save
        self.ga = GA(Config(
            gene_pattern=[FloatItem(-2, 2, 10) for _ in range(self.n)],
            fit=lambda data: 1 / (self.fit(data) + 0.001),
            max_gen=gen,
        ))

    def update(self, ga: GA):
        values = [item.fitness for item in ga.chromosomes]
        self.gen.append(ga.generation)
        self.best.append(ga.best().raw_fitness)
        self.mean.append(np.mean(values))

    def plot(self):
        plt.rcParams['font.family'] = 'CMU Serif'
        plt.rcParams['font.size'] = 14
        fig = plt.figure(dpi=100, figsize=(10, 5))
        for i in range(self.n):
            ax = fig.add_subplot(self.grid[0, i])
            ax.plot([item.genes[i] for item in self.ga.chromosomes], '.k', markersize=2)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_xticklabels([])

            if i > 0:
                ax.set_yticks([])
                ax.set_yticklabels([])
            else:
                ax.set_ylabel('Normalised Gene Value')

        best_gen = fig.add_subplot(self.grid[1, :])
        best_gen.plot(self.gen, self.best, '-k', label='Best', linewidth=1)
        best_gen.plot(self.gen, self.mean, '--k', label='Mean', linewidth=1)
        best_gen.set_xlabel('Number of Generation')
        best_gen.set_ylabel('Fitness Value')
        best_gen.legend(frameon=False)

        fig.tight_layout(h_pad=0.5, w_pad=0.1)
        if self.save:
            fig.savefig(self.title + '.pdf')
        else:
            plt.show()

    def run(self):
        self.ga.evolve(self.update)

        best_individual = self.ga.best()
        best_ans = best_individual.decode()
        best_result = self.fit(best_ans)

        if self.title:
            print(f'Problem:  min({self.title})')
        print(f'BEST:     {best_ans}\n'
              f'RESULT:   {best_result}\n'
              f'FIT:      {best_individual.raw_fitness}')
        if not self.noplot:
            self.plot()

        return best_ans, best_result, best_individual.raw_fitness


def stats(bests, results, fitnesses):
    print(f'ANSWER AVG: {np.mean(bests)}')
    print(f'ANSWER STD: {np.std(bests)}')
    print(f'RESULT AVG: {np.mean(results)}')
    print(f'RESULT STD: {np.std(results)}')
    print(f'FIT    AVG: {np.mean(fitnesses)}')
    print(f'FIT    STD: {np.std(fitnesses)}')


def run_multiple_times(pid, bests, results, fitnesses, n=10):
    for i in range(n):
        # a, b, c = GAPlot(n=3, gen=300, fit=sphere, noplot=True).run()
        # a, b, c = GAPlot(n=3, gen=300, fit=rosenbrock, noplot=True).run()
        a, b, c = GAPlot(n=3, gen=300, fit=rastrigin, noplot=True).run()
        index = pid * 10 + i

        # only for rosenbrock
        # bests[index] = np.linalg.norm(np.array([1]*len(a)) - np.array(a))

        bests[index] = np.linalg.norm(np.array(a))
        results[index] = b
        fitnesses[index] = c
        print(f'===== Worker {pid}: {i + 1}/{n}')


def run_ex_with_multiple_cpu_cores():
    processes = []
    bests = mp.Array('d', 100)
    results = mp.Array('d', 100)
    fitnesses = mp.Array('d', 100)
    for i in range(10):
        t = mp.Process(target=run_multiple_times, args=(i, bests, results, fitnesses, 2))
        processes.append(t)
        t.start()

    for item in processes:
        item.join()

    stats(bests[:], results[:], fitnesses[:])


if __name__ == '__main__':
    run_ex_with_multiple_cpu_cores()
