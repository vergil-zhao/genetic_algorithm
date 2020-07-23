# A Python Implementation of GA

A Python implementation of genetic algorithm contains multiple operators of different stages for tuning.

## Structure

```
genetic_algorithm
 ├ ga
 │  ├ conf.py --------- Configuration class for setting up GA parameters and
 │  │                   operators including crossover rate, mutation rate, etc.
 │  │
 │  ├ genetic.py ------ Chromosome class containing genes
 │  │
 │  └ popluation.py --- Main algorithm
 │
 ├ operators
 │  ├ selection.py ---- Selection operators for creating mating pool
 │  │                   in which individuals can be choose to mate.
 │  │                   Contains roulette, tournament, etc.
 │  │
 │  ├ mating.py ------- Mating operators, the way how to choose two individuals
 │  │                   in the mating pool. Contains random, phonetypic, etc.
 │  │
 │  ├ crossover.py ---- Crossover operators control how the genes of offsprings 
 │  │                   are derived from parents. Contains single point, SBX, etc.
 │  │
 │  ├ mutation.py ----- Mutation operators control how the genes of offsprings mutate.
 │  │                   Contains random, normal distribution, etc.
 │  │
 │  └ elimination.py -- Elimination operators control which parent will be 
 │                      eliminated and replaced by offsprings for next generation. 
 │                      Contains fitness, age, etc.
 └ tests
```  

## Main Algorithm

```
    ┌─────────────────────┐
    │        Start        │
    └─────────────────────┘        
               ↓
    ┌─────────────────────┐
    │   Initialization    │  generate chromosomes
    └─────────────────────┘
               ↓
    ┌─────────────────────┐
 ┌─>│  Diversity Control  │  TODO
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │       Scaling       │  TODO
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │      Selection      │  create a mating pool for offsprings
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │       Mating        │  parents mating by specific way
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │      Crossover      │  chromosome crossover and produce offsprings
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │       Mutation      │  offspings mutate
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │      Evalution      │  fitness evaluation
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 │  │     Replacement     │  put offsprings back to population
 │  └─────────────────────┘
 │             ↓
 │  ┌─────────────────────┐
 └──│      Satisfied?     │ 
 NO └─────────────────────┘
           YES ↓ 
    ┌─────────────────────┐
    │         End         │
    └─────────────────────┘
```

## TODO
- [x] Add `setup.py`  for packaging and commands
- [ ] Add Travis CI config
- [x] Saving states for passive call
- [ ] Diversity Control
- [ ] Scaling (adding evolution pressure)
- [ ] Add different stop criteria
- [ ] Implement Multi-Objective


## Reference
- [1] Sudhoff, S. D. (2014). Genetic Optimization System Engineering Toolbox 2.6. Retrieved June 20, 2020, from https://engineering.purdue.edu/ECE/Research/Areas/PES/genetic-optimization-toolbox-2.6
- [2] Sivanandam, S. N., & Deepa, S. N. (2008). [Genetic algorithms](https://link.springer.com/content/pdf/10.1007/978-3-540-73190-0_2.pdf). In Introduction to genetic algorithms (pp. 15-37). Springer, Berlin, Heidelberg.
- [3] Deb, K., & Agrawal, R. B. (1995). [Simulated binary crossover for continuous search space.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.26.8485&rep=rep1&type=pdf) Complex systems, 9(2), 115-148.
- [4] Janikow, C. Z., & Michalewicz, Z. (1991, July). [An experimental comparison of binary and floating point representations in genetic algorithms](http://www.cs.umsl.edu/~janikow/publications/1991/GAbin/text.pdf). In ICGA (Vol. 1991, pp. 31-36).
- [5] Tomasz, D., 2006. [Genetic Algorithms Reference](https://dl.acm.org/doi/book/10.5555/1203159). Tomasz Gwiazda, p.20.