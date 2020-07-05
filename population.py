from __future__ import annotations

import random

from typing import List, Optional, Callable
from collections import Iterable
from math import floor

from genetic import FloatItem, Chromosome
from operators.selection import rank
from operators.elimination import fitness_tournament
from utils import prettify_matrix


class Population(Iterable):
    def __init__(
            self,
            gene_pattern: List[FloatItem],
            fit: Callable[[List[float]], float],
            size: int = 10,
            crossover_rate: float = 0.8,
            mutation_rate: float = 0.05,
            elitism: int = 0,
            max_gen: int = 100,
            selection: Callable[[List[Chromosome], int], List[Chromosome]] = rank,
            elimination: Callable[[List[Chromosome], int], None] = fitness_tournament
    ):
        """
        Create a GA instance

        :param gene_pattern: specify the condition of individual(s), FLoatItem, list of FloatItem
        :param size: an int indicating the number of the population
        :param crossover_rate: how many population will be involved to crossover for offsprings, float 0 - 1
        :param mutation_rate: how big the change the offsprings will be mutate, float 0 - 1
        :param fit: a function receives a raw data and returns a fitness number, float 0 - 1
        :param elitism: keep the best n items for next iteration
        :param max_gen: maximum generations, 0 means no limit
        """
        if gene_pattern is None:
            raise ValueError('"pattern" has to be a list of item, eg. [FloatItem(min=0.1, max=1, precision=8)]')
        elif isinstance(gene_pattern, list):
            if len(gene_pattern) == 0:
                raise ValueError('"pattern" cannot be empty')
            for c in gene_pattern:
                if not isinstance(c, FloatItem):
                    raise ValueError('the value of "pattern" could only be FloatItem')
        elif not isinstance(gene_pattern, FloatItem):
            raise TypeError('"pattern" now could only be a FloatItem or a list of FloatItem')

        self.gene_pattern = gene_pattern
        self.size = size
        self.pool_size: int = floor(size * (crossover_rate if crossover_rate <= 1 else 1))
        self.mutation_rate = mutation_rate if mutation_rate <= 1 else 1
        self.fit = fit
        self.elitism = elitism if elitism <= size else size
        self.max_gen = max_gen
        self.generations = 0
        self.selection = selection
        self.elimination = elimination

        self.chromosomes: List[Chromosome] = []
        self.offsprings: List[Chromosome] = []
        self.generate_population()

    # TODO: Real-coded, Binary
    @staticmethod
    def encode(value):
        return value

    @staticmethod
    def decode(chromosome):
        return chromosome

    def generate_population(self):
        for i in range(self.size):
            self.chromosomes.append(Chromosome(pattern=self.gene_pattern))

    def create_mating_pool(self) -> List[Chromosome]:
        return self.selection(self.chromosomes, self.pool_size)

    def age_grow(self):
        for item in self.chromosomes:
            item.age += 1

    def eliminate(self):
        self.elimination(self.chromosomes, self.pool_size)

    def replace(self):
        i = 0
        for offspring in self.offsprings:
            while i < len(self.chromosomes) and self.chromosomes[i].is_alive:
                i += 1
            self.chromosomes[i] = offspring

    def sample(self, k: int) -> List[Chromosome]:
        if k > len(self.chromosomes):
            raise ValueError('k cannot be larger than the population')

        result = []
        while len(result) < k:
            c = random.choice(self.chromosomes)
            if c.is_alive:
                result.append(c)
        return result

    def get_result(self):
        return [self.decode(p) for p in self.chromosomes]

    # TODO: Different way to apply crossover, Single Point, SBC, etc.
    def crossover(self):
        mating_pool = self.create_mating_pool()
        self.offsprings = []
        for i in range(0, len(mating_pool), 2):
            a, b = mating_pool[i] + mating_pool[i + 1]
            self.offsprings.append(a)
            self.offsprings.append(b)

    # TODO: Different way to apply mutation, Random, Random with a vicinity, Normally Distributed
    def mutate(self):
        for offspring in self.offsprings:
            offspring.mutate(self.mutation_rate, self.gene_pattern)

    # TODO: add passively accept fitness value
    def evaluate(self, individuals: List[Chromosome]):
        for i in individuals:
            i.fitness = self.fit(list(i.genes))

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
        return self.generations >= self.max_gen

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
