from dataclasses import dataclass
from typing import List, Callable, Tuple, Any
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
        :param end: the maximum value of the individual
        :param precision: it is the number of bits when GA uses binary encoding,
                          it is the number of digits after point when GA uses real-coding
        """
        assert start < end
        assert precision >= 0

        self.start = start
        self.end = end
        self.precision = precision


@dataclass
class Config:
    def __init__(
            self,
            gene_pattern: List[FloatItem],
            fit: Callable[[List[float]], float],
            size: int = 10,
            crossover_rate: float = 0.8,
            mutation_rate: float = 0.05,
            elitism: int = 0,
            max_gen: int = 100,
            selection: Callable[[List, int], List] = sel.fitness_tournament,
            elimination: Callable[[List, int], None] = eli.fitness_tournament,
            mating: Callable[[List], List] = mat.random_mating_once,
            crossover: Callable[[List[float], List[float]], Tuple[List[float], List[float]]] = cro.sbx,
            mutation: Callable[[List[float], float, Any], List[float]] = mut.norm_dist
    ):
        """
        Create a GA Config

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
        self.selection = selection
        self.elimination = elimination
        self.mating = mating
        self.crossover = crossover

        def m(genes: List[float], **kwargs) -> List[float]:
            return mutation(genes, self.mutation_rate, **kwargs)
        self.mutation = m
