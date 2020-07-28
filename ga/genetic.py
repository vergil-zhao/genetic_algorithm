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

from __future__ import annotations

import random

from typing import List, Optional
from collections import Iterable
from operators.utils import repair

from .conf import Config


class Chromosome(Iterable):
    """
    A chromosome contains a serial of genes represented in numbers.
    The gene is a real number from 0 to 1 mapped from actual parameters.
    """

    def __init__(
            self,
            config: Config,
            genes: Optional[List[float]] = None
    ):
        """
        Create a new Chromosome with Config

        :param config: GA Config
        :param genes: list of real numbers from 0 to 1, it will be repaired by '% 1' if not in the range
        """
        self.age = 0
        self.is_alive = True
        self.fitness = 0.0
        self.penalty = 1.0
        self.config = config
        if genes is not None:
            self.genes = repair(genes)
        else:
            self.generate()

    @property
    def raw_fitness(self):
        return self.__fitness

    @property
    def fitness(self):
        if self.config.diversity_control:
            return self.__fitness * self.penalty
        return self.__fitness

    @fitness.setter
    def fitness(self, value: float):
        assert value >= 0
        self.__fitness = float(value)

    def generate(self):
        """Generate and replace genes randomly"""
        self.genes = []
        for _i in range(len(self.config.gene_pattern)):
            self.genes.append(random.random())

    def mutate(self, **kwargs):
        """
        Mutate genes. Every gene has same probability to mutate.
        """
        self.genes = repair(self.config.mutation(self.genes, **kwargs))

    def update(self, data: dict):
        """
        Encode from original parameters and update it to genes

        :param data: original actual parameters, fitness value and alive or not
        """
        parameters = data.get('parameters')
        assert parameters is not None
        assert len(parameters) == len(self.config.gene_pattern), 'incompatitive parameters'

        alive = data.get('alive')
        assert isinstance(alive, bool)

        result = []
        for i, item in enumerate(self.config.gene_pattern):
            result.append((parameters[i] - item.start) / (item.end - item.start))
        self.genes = repair(result)
        self.fitness = data.get('fitness')
        self.is_alive = alive

    @staticmethod
    def from_dict(config: Config, data: dict):
        result = Chromosome(config)
        result.update(data)
        return result

    def decode(self) -> List[float]:
        """
        Decode genes to actual parameters

        :return: actual parameters
        """
        # TODO: Logarithmic map to 0 - 1
        result = []
        for i, item in enumerate(self.config.gene_pattern):
            result.append(round(self.genes[i] * (item.end - item.start) + item.start, item.precision))
        return result

    def serialize(self) -> dict:
        return {
            'parameters': self.decode(),
            'fitness': self.fitness,
            'alive': self.is_alive,
        }

    def __add__(self, other: Chromosome) -> (Chromosome, Chromosome):
        """
        Two chromosome mating & crossover

        :param other: another Chromosome
        :return: two offsprings
        """
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
