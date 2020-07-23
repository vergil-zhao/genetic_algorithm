from __future__ import annotations

from dataclasses import dataclass
from typing import List, Callable, Tuple, Any, Optional
from math import floor

import operators.selection as sel
import operators.mating as mat
import operators.elimination as eli
import operators.crossover as cro
import operators.mutation as mut


@dataclass
class FloatItem:
    def __init__(self, start: float, end: float, precision: int):
        """
        An individual condition

        :param start: the minimum value of the individual
        :param end: the maximum value (not include) of the individual
        :param precision: it is the number of bits when GA uses binary encoding,
                          it is the number of digits after point when GA uses real-coding
        """
        assert start < end
        assert precision >= 0

        self.start = start
        self.end = end
        self.precision = precision

    @staticmethod
    def from_dict(data: dict):
        return FloatItem(
            start=data.get('start'),
            end=data.get('end'),
            precision=data.get('precision')
        )

    def serialize(self):
        return {
            'start': self.start,
            'end': self.end,
            'precision': self.precision,
        }


@dataclass
class Config:
    def __init__(
            self,
            gene_pattern: List[FloatItem],
            fit: Optional[Callable[[List[float]], float]] = None,
            size: int = 100,
            crossover_rate: float = 0.8,
            mutation_rate: float = 0.05,
            elitism: bool = True,
            max_gen: int = 100,
            selection: Callable[[List, int], List] = sel.fitness_tournament,
            elimination: Callable[[List, int], None] = eli.fitness_tournament,
            mating: Callable[[List], List] = mat.phenotypic_mating,
            crossover: Callable[[List[float], List[float]], Tuple[List[float], List[float]]] = cro.sbx,
            mutation: Callable[[List[float], float, Any], List[float]] = mut.norm_dist,
            mutation_sigma: float = 0.2,
            shrink_mutation_range: bool = True,
    ):
        """
        Create a GA Config

        :param gene_pattern: Specify the condition of individual(s), FLoatItem, list of FloatItem
        :param fit: A function should receives actual data and returns a fitness number
        :param size: An int indicating the number of the population
        :param crossover_rate: How many population will be involved to crossover for offsprings, float (0, 1]
                                The size of mating pool will be always an even number. It has to be high enough
                                to make the pool size larger than 0.
        :param mutation_rate: How big the change the offsprings will be mutate, float [0, 1]
        :param elitism: Keep the best n items for next iteration
        :param max_gen: Maximum generations, 0 means no limit
        :param selection: Selection operator
        :param elimination: Elimination operator
        :param mating: Mating operator
        :param crossover: Crossover operator
        :param mutation: Mutation operator
        :param mutation_sigma: The sigma value for normal distribution, only effective when operator is norm_dist
        :param shrink_mutation_range: Change mutation_sigma gradually by every generation
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

        assert size >= 2, 'size less than 2 is meaningless'
        assert max_gen > 0, '0 max generation is meaningless'

        pool_size = int(floor(size * (crossover_rate if crossover_rate <= 1 else 1)))
        pool_size = pool_size - (pool_size % 2)
        assert pool_size > 0, 'crossover rate is too low to build a valid mating pool'

        self.gene_pattern = gene_pattern
        self.size = size
        self._crossover_rate = crossover_rate
        self.pool_size = pool_size
        self.mutation_rate = mutation_rate if mutation_rate <= 1 else 1
        self.fit = fit
        self.elitism = elitism if elitism <= size else size
        self.max_gen = max_gen
        self.selection = selection
        self.elimination = elimination
        self.mating = mating
        self.crossover = crossover
        self._mutation = mutation
        self.mutation_sigma = mutation_sigma
        self.shrink_mutation_range = shrink_mutation_range

        def m(genes: List[float], **kwargs) -> List[float]:
            return self._mutation(genes, self.mutation_rate, **kwargs)
        self.mutation = m

    @staticmethod
    def from_dict(data: dict) -> Config:
        pattern = data.get('pattern')
        assert isinstance(pattern, list)

        return Config(
            gene_pattern=[FloatItem.from_dict(item) for item in pattern],
            size=data.get('size') or 100,
            crossover_rate=data.get('crossoverRate') or 0.8,
            mutation_rate=data.get('mutationRate') or 0.05,
            elitism=data.get('elitism') or 1,
            max_gen=data.get('maxGen') or 100,
        )

    def serialize(self):
        return {
            'pattern': [item.serialize() for item in self.gene_pattern],
            'size': self.size,
            'crossoverRate': self._crossover_rate,
            'mutationRate': self.mutation_rate,
            'elitism': self.elitism,
            'maxGen': self.max_gen,
            # 'selection': {
            #     'operator': None,
            #     'tournament': None,
            # },
            # 'elimination': {
            #     'operator': None,
            #     'tournament': None,
            # },
            # 'mating': {
            #     'operator': None,
            # },
            # 'crossover': {
            #     'operator': None,
            #     'alpha': None,
            #     'eta': None,
            # },
            # 'mutation': {
            #     'operator': None,
            #     'sigma': self.mutation_sigma,
            #     'shrink': self.shrink_mutation_range,
            # },
        }
