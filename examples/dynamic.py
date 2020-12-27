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

from examples.functions import sphere, rosenbrock, rastrigin
from matplotlib.gridspec import GridSpec
from ga.algorithms import GA
from ga.conf import FloatItem, Config


def run(gene_len=5, max_gen=200, problem=rastrigin):
    p = GA(Config(
        gene_pattern=[FloatItem(-2, 2, 10) for _ in range(gene_len)],
        fit=lambda data: 1 / (problem(data) + 0.001),
        max_gen=max_gen,
    ))

    gs = GridSpec(2, gene_len)

    fig = plt.figure()
    fig.suptitle('min(rosenbrock)')

    ps = []
    for i in range(gene_len):
        ax = plt.subplot(gs[0, i])
        pl, = ax.plot([item.genes[i] for item in p.chromosomes], '.')
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_xticklabels([])

        if i > 0:
            ax.set_yticks([])
            ax.set_yticklabels([])
        else:
            ax.set_ylabel('Normalized Gene Value')

        ps.append(pl)

    ax3 = plt.subplot(gs[1, :])
    x_data, y_data, mean = [], [], []
    p2, = ax3.plot([], [], label='Best')
    p3, = ax3.plot([], [], label='Mean')
    ax3.set_xlim(1, max_gen)
    ax3.set_ylim(0, 1000)
    ax3.set_xlabel('Generation')
    ax3.set_ylabel('Fitness')
    ax3.legend()

    plt.subplots_adjust(wspace=0)

    def update(ga: GA):
        for i in range(gene_len):
            ps[i].set_ydata([item.genes[i] for item in ga.chromosomes])
        x_data.append(ga.generation)
        y_data.append(ga.best().raw_fitness)
        mean.append(np.mean([c.raw_fitness for c in ga.chromosomes]))
        p2.set_xdata(x_data)
        p2.set_ydata(y_data)
        p3.set_xdata(x_data)
        p3.set_ydata(mean)
        plt.pause(1e-20)

    p.evolve(update)

    best_individual = p.best()
    best_ans = best_individual.decode()
    print(f'BEST:   {best_ans}\n'
          f'RESULT: {problem(best_ans)}\n'
          f'FIT:    {best_individual.raw_fitness}')

    plt.show()


if __name__ == '__main__':
    run()
