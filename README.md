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
 └──│      Satisfied?     │ 
 NO └─────────────────────┘
           YES ↓ 
    ┌─────────────────────┐
    │         End         │
    └─────────────────────┘
```

## TODO
- [ ] Add setup.py 
- [ ] Saving states for passive call
- [ ] Diversity Control
- [ ] Scaling (adding evolution pressure)


## Reference
[1] [Genetic Optimization System Engineering Toolbox - Purdue University](https://engineering.purdue.edu/ECE/Research/Areas/PES/genetic-optimization-toolbox-2.6)
