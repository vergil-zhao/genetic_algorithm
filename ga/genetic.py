from __future__ import annotations

import random

from typing import List, Optional
from collections import Iterable
from operators.utils import repair

from .conf import Config


class Chromosome(Iterable):
    def __init__(
            self,
            config: Config,
            genes: Optional[List[float]] = None
    ):
        self.age = 0
        self.is_alive = True
        self.fitness = 0.0
        self.config = config
        self.genes = genes
        if genes is None:
            self.generate()

    def generate(self):
        self.genes = []
        for _i in range(len(self.config.gene_pattern)):
            self.genes.append(random.random())

    # TODO: different distribution of random mutation
    def mutate(self, **kwargs):
        self.genes = repair(self.config.mutation(self.genes, **kwargs))

    def decode(self) -> List[float]:
        # TODO: Linear/logarithmic map to 0 - 1
        result = []
        for i, item in enumerate(self.config.gene_pattern):
            result.append(round(self.genes[i] * (item.end - item.start) + item.start, item.precision))
        return result

    # TODO: Different way to apply crossover, Blend, SBC, etc.
    def __add__(self, other: Chromosome) -> (Chromosome, Chromosome):
        a, b = self.config.crossover(self.genes, other.genes)
        return Chromosome(self.config, repair(a)), Chromosome(self.config, repair(b))

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
        return str(self.decode())
