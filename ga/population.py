from __future__ import annotations

from typing import List, Optional, Callable
from collections import Iterable

from operators.utils import prettify_matrix

from .genetic import Chromosome
from .conf import Config


class Population(Iterable):
    """
    Popluation is the main class of this genetic algorthim implementation.
    It contains fixed size of chromosomes after initialized.

    Algorithm Process:
    Start
        ↓
    Initialization: generate chromosomes
        ↓
    * Diversity Control: TODO
        ↓
    Scaling: TODO
        ↓
    Selection: create a mating pool for offsprings
        ↓
    Mating: parents mating by specific way
        ↓
    Crossover: chromosome crossover and produce offsprings
        ↓
    Mutation: offspings mutate
        ↓
    Evalution: fitness evaluation
        ↓
    Satisfied? -> If no, go back to *
        ↓
    End

    """

    def __init__(self, config: Config, chromosomes: Optional[List[Chromosome]] = None):
        """
        Create a population for running genetic algorithm

        :param config: GA Config
        :param chromosomes: initial chromosomes, can be used to continue last running
        """
        self.config = config
        self.generations = 0
        self.chromosomes: List[Chromosome] = [] if chromosomes is None else chromosomes
        self.offsprings: List[Chromosome] = []
        if chromosomes is None:
            self.generate_population()

    def generate_population(self):
        """
        Generation specific size of chromosomes
        :return:
        """
        for i in range(self.config.size):
            self.chromosomes.append(Chromosome(self.config))

    def create_mating_pool(self) -> List[Chromosome]:
        return self.config.selection(self.chromosomes, self.config.pool_size)

    def age_grow(self):
        for item in self.chromosomes:
            item.age += 1

    def eliminate(self):
        self.config.elimination(self.chromosomes, self.config.pool_size)

    def crossover(self):
        mating_pool = self.create_mating_pool()
        self.offsprings = self.config.mating(mating_pool)

    def mutate(self):
        if self.config.shrink_mutation_range:
            sigma = (1 - self.generations / self.config.max_gen) * self.config.mutation_sigma
        else:
            sigma = self.config.mutation_sigma
        for offspring in self.offsprings:
            offspring.mutate(sigma=sigma)

    # TODO: add passively accept fitness value
    # TODO: scaling, add evolution pressure
    def evaluate(self, chromosomes: List[Chromosome]):
        for i in chromosomes:
            i.fitness = self.config.fit(list(i.decode()))

    def keep_elitist(self):
        best_parent = max(self.chromosomes)
        best_child = max(self.offsprings)

        if best_parent > best_child:
            best_parent.is_alive = True
            self.offsprings.remove(best_child)

    def replace(self):
        if self.config.elitism > 0:
            self.keep_elitist()

        i = 0
        for offspring in self.offsprings:
            while i < len(self.chromosomes) and self.chromosomes[i].is_alive:
                i += 1
            assert i < len(self.chromosomes)
            self.chromosomes[i] = offspring

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

    def evolve(self, callback: Optional[Callable[[Population], None]] = None) -> None:
        """
        Main method for running genetic algorithm, actively call a fitness function

        :param callback: a function called every generation
        """
        self.generations = 0
        self.evaluate(self.chromosomes)
        callback(self) if callback is not None else None
        # TODO: different way to stop
        # TODO: diversity control
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
        return prettify_matrix([c.decode() for c in self.chromosomes])
