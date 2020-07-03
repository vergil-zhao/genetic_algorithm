from __future__ import annotations

import random

from typing import List, Optional, Callable, Tuple
from collections import Iterable
from dataclasses import dataclass

from operators.crossover import single_point


@dataclass
class FloatItem:
    """
    An individual condition

    Args:
        min (float): the minimum value of the individual
        max (float): the maximum value of the individual
        precision (int): it is the number of bits when GA uses binary encoding,
                         it is the number of digits after point when GA uses real-coding
    """
    min: float
    max: float
    precision: int


class Chromosome(Iterable):
    def __init__(
            self,
            genes: Optional[List[float]] = None,
            pattern: Optional[List[FloatItem]] = None,
            crossover: Callable[[List[float], List[float]], Tuple[List[float], List[float]]] = single_point
    ):
        self.age = 0
        self.is_alive = True
        self.fitness = 0.0
        self.genes = genes
        self.crossover = crossover
        if pattern is not None and genes is None:
            self.generate(pattern)

    def generate(self, pattern: List[FloatItem]):
        self.genes = []
        for param in pattern:
            self.genes.append(round(random.uniform(param.min, param.max), param.precision))

    # TODO: different distribution of random mutation
    def mutate(self, rate: float, pattern: List[FloatItem]):
        for i in range(len(self.genes)):
            if rate > random.random():
                self.genes[i] = round(random.uniform(pattern[i].min, pattern[i].max), pattern[i].precision)

    # TODO: different way to cut the chromosome
    def __add__(self, other: Chromosome) -> (Chromosome, Chromosome):
        a, b = self.crossover(self.genes, other.genes)
        return Chromosome(a), Chromosome(b)

    def __gt__(self, other: Chromosome):
        return self.fitness > other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __getitem__(self, item: int) -> float:
        return self.genes[item]

    def __setitem__(self, key: int, value: float):
        self.genes[key] = value

    def __iter__(self):
        return iter(self.genes)

    def __repr__(self):
        return str(self.genes)
