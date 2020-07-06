from __future__ import annotations

from typing import List, Optional, Callable
from collections import Iterable

from operators.utils import prettify_matrix

from .genetic import Chromosome
from .conf import Config


class Population(Iterable):
    def __init__(self, config: Config):
        self.config = config
        self.generations = 0
        self.chromosomes: List[Chromosome] = []
        self.offsprings: List[Chromosome] = []
        self.generate_population()

    def generate_population(self):
        for i in range(self.config.size):
            self.chromosomes.append(Chromosome(self.config))

    def create_mating_pool(self) -> List[Chromosome]:
        return self.config.selection(self.chromosomes, self.config.pool_size)

    def age_grow(self):
        for item in self.chromosomes:
            item.age += 1

    def eliminate(self):
        self.config.elimination(self.chromosomes, self.config.pool_size)

    def replace(self):
        i = 0
        for offspring in self.offsprings:
            while i < len(self.chromosomes) and self.chromosomes[i].is_alive:
                i += 1
            self.chromosomes[i] = offspring

    def crossover(self):
        mating_pool = self.create_mating_pool()
        self.offsprings = []
        for i in range(0, len(mating_pool), 2):
            a, b = mating_pool[i] + mating_pool[i + 1]
            self.offsprings.append(a)
            self.offsprings.append(b)

    def mutate(self):
        for offspring in self.offsprings:
            offspring.mutate()

    # TODO: add passively accept fitness value
    # TODO: scaling, add evolution pressure
    def evaluate(self, individuals: List[Chromosome]):
        for i in individuals:
            i.fitness = self.config.fit(list(i.genes))

    def rescale_fitness(self):
        data = [item.fitness for item in self.chromosomes]
        largest = max(data)
        smallest = min(data)
        difference = largest - smallest
        if difference == 0:
            difference = 1
        return [(i - smallest) / difference for i in data]

    # TODO: Standard Deviation?
    def is_satisfied(self):
        # data = self.rescale_fitness()
        # print(f'FIT:  {data}')
        # print(f'MEAN: {statistics.mean(data)}')
        # print(f'STD:  {statistics.stdev(data)}')
        # return statistics.stdev(data) < 0.1
        return self.generations >= self.config.max_gen

    def evolve(self, callback: Optional[Callable[[Population], None]] = None):
        self.generations = 0
        self.evaluate(self.chromosomes)
        callback(self) if callback is not None else None
        # TODO: different way to stop
        while not self.is_satisfied():
            self.generations += 1
            self.age_grow()
            self.eliminate()
            self.crossover()
            self.mutate()
            self.replace()
            # TODO: passively trigger every iteration
            self.evaluate(self.offsprings)
            callback(self) if callback is not None else None

    def __getitem__(self, item: int) -> Chromosome:
        return self.chromosomes[item]

    def __setitem__(self, key: int, value: Chromosome):
        self.chromosomes[key] = value

    def __iter__(self):
        return iter(self.chromosomes)

    def __repr__(self):
        return prettify_matrix(self)
