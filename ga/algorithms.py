from __future__ import annotations

from typing import List, Optional, Callable, NamedTuple
from collections import Iterable

from operators.utils import prettify_matrix

from .genetic import Chromosome
from .conf import Config


class GA(Iterable):
    """
    GA is the main class of this genetic algorthim implementation.
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
        self.generation = 0
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
            sigma = (1 - self.generation / self.config.max_gen) * self.config.mutation_sigma
        else:
            sigma = self.config.mutation_sigma
        for offspring in self.offsprings:
            offspring.mutate(sigma=sigma)

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
        if self.config.elitism:
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
    def is_satisfied(self) -> bool:
        # data = self.rescale_fitness()
        # print(f'FIT:  {data}')
        # print(f'MEAN: {statistics.mean(data)}')
        # print(f'STD:  {statistics.stdev(data)}')
        # return statistics.stdev(data) < 0.1
        return self.generation >= self.config.max_gen

    def evolve(self, callback: Optional[Callable[[GA], None]] = None) -> None:
        """
        Main method for running genetic algorithm, actively call a fitness function

        :param callback: a function called every generation
        """
        self.generation = 0
        self.evaluate(self.chromosomes)
        callback(self) if callback is not None else None
        # TODO: different way to stop
        # TODO: diversity control
        while not self.is_satisfied():
            self.generation += 1
            self.age_grow()
            self.crossover()
            self.mutate()
            self.evaluate(self.offsprings)
            self.eliminate()
            self.replace()
            callback(self) if callback is not None else None

    def __getitem__(self, item: int) -> Chromosome:
        return self.chromosomes[item]

    def __setitem__(self, key: int, value: Chromosome):
        self.chromosomes[key] = value

    def __iter__(self):
        return iter(self.chromosomes)

    def __repr__(self):
        return prettify_matrix([c.decode() for c in self.chromosomes])


class GAPassive(GA):
    """
    GAPassive accept fitness from exterior when generations is not 0.
    It will not evaluate fitness after evolved, so evolve should be
    called only once.
    """

    def __init__(
            self,
            config: Config,
            generation: int = 0,
            population: Optional[List[Chromosome]] = None,
            offsprings: Optional[List[Chromosome]] = None,
    ):

        assert len(population) == config.size

        super().__init__(config, population)
        self.generation = generation
        self.offsprings = offsprings or []
        self._satisfied = None

        if self.generation > 0:
            assert len(self.offsprings) > 0

    def is_satisfied(self) -> bool:
        if self._satisfied is None:
            self._satisfied = super().is_satisfied()
        return self._satisfied

    def evolve(self, callback: Optional[Callable[[GA], None]] = None) -> None:
        if self.is_satisfied():
            return
        self.replace() if self.generation > 0 else None
        self.generation += 1
        self.age_grow()
        self.crossover()
        self.mutate()
        self.eliminate()

    @staticmethod
    def from_dict(config_data: dict, data: Optional[dict] = None):
        config = Config.from_dict(config_data)
        if data is None:
            return GAPassive(config)

        generation = data.get('generation')
        assert generation is not None
        assert isinstance(generation, int)
        assert generation >= 0

        population = data.get('population')
        assert population is not None
        assert len(population) == config.size

        offsprings = data.get('offsprings') or []

        return GAPassive(
            config,
            generation,
            [Chromosome.from_dict(config, item) for item in population],
            [Chromosome.from_dict(config, item) for item in offsprings],
        )

    def serialize(self) -> dict:
        return {
            'population': [item.serialize() for item in self.chromosomes],
            'offsprings': [item.serialize() for item in self.offsprings],
            'generation': self.generation,
            'satisfied': self.is_satisfied(),
        }
