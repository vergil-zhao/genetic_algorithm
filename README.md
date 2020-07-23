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
 │  └ algorithms.py --- Main algorithm GA and GAPassive
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
 │
 ├ cli
 │
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

## Installation
You can install it by clone this repo and run the installation command.
```shell script
git clone https://github.com/vergilchoi/genetic_algorithm
```

Install locally by using pip:
```shell script
pip install .
```

Install locally by using python:
```shell script
python setup.py install
```

## Use as a command

### Config

A configuration file is need to be like this:
```yaml
# config.yml

pattern:                # specify the parameter range
  - start: 0            # the lower bound
    end: 1              # the higher bound (not include)
    precision: 10       # indicates how many digits after point will be kept
  - start: 0
    end: 2
    precision: 10
  - start: 0
    end: 3
    precision: 10
size: 5                 # population size
crossoverRate: 0.75     # indicates how big the mating pool size is, (0, 1]
mutationRate: 0.06      # the probability of mutation for every gene, [0, 1]
elitism: true           # keep the elitist or not
maxGen: 100             # max generation
```

### Input and Output

Result can be store in a single file or in a directory which will contain every generation. The output format will be like below:

```json
{
  "population": [
    {
      "parameters": [0.0, 0.0, 0.0],  // actual parameters
      "fitness": 1.0,                 // fitness value
      "alive": true                   // The alive flag. It will be kept for next
                                      // generation if it true, otherwise, it may
                                      // be replaced by offspring.
    },
    ...
  ],
  "offsprings": [
    {
      "parameters": [0.0, 0.0, 0.0],  // Using this to run a your function/program
      "fitness": 1.0,                 // then fill the fitness value here
      "alive": true
    },
    ...
  ],
  "generation": 10,
  "satisfied": false                  // If it is true, the algorithm will not run.
                                      // It will be set to true if algorithm find it
                                      // is satisfied. (It means the max generation 
                                      // has reached for now.)
}
```

### Commands

To run it with a single file:

```shell script
# read data from data.json and store result to the same file for next run 
genetic run -c config.yml -i data.json

# read data from input_data.json and store result to output_data.json
genetic run -c config.yml -i input_data.json -o output_data.json
```

If the input file/directory is not exist, the algorithm will generate initial population and create the file/directory if possible.

If a directory specified, it will read the last file in the directory, which is ordered by file names. The output files will be named as generation number.

```shell script
# read the last data from the directory specified
# and store the result to the same directory
genetic run -c config.yml -i ./data/

# using different directory
genetic run -c config.yml -i ./input_data/ -o ./output_data/
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