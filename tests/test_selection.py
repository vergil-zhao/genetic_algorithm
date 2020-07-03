from operators.selection import *
from genetic import Chromosome, FloatItem

pattern = [
    FloatItem(0, 10, 5),
    FloatItem(0, 10, 5),
    FloatItem(0, 10, 5)
]

chromosomes = [Chromosome(pattern=pattern) for _i in range(10)]

for i in range(10):
    chromosomes[i].fitness = i


def test(func):
    def wrapper():
        print(func.__name__)
        func()
    return wrapper


@test
def test_random_pick():
    print([c.fitness for c in random_pick(chromosomes, 5)])


@test
def test_roulette_wheel():
    print([c.fitness for c in roulette_wheel(chromosomes, 5)])


@test
def test_tournament():
    print([c.fitness for c in tournament(chromosomes, 5)])


if __name__ == '__main__':
    test_random_pick()
    test_roulette_wheel()
    test_tournament()
