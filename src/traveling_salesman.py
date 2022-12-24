# coding: utf-8

import copy
import random
import time

import numpy as np
from pandas import read_csv

from src.models.chromosome import Chromosome
from src.models.fitness import Fitness
from src.models.mutation import Mutation
from src.models.selection import Selection


class TravelingSalesman:
    def __init__(self, file_name):
        data = read_csv(file_name, header=None).to_numpy()
        Chromosome.FitnessModule = Fitness
        Chromosome.FitnessModule.initialize_matrix(data)

        self.num_genes = len(data)

    def simple_genetic_algorithm(self, population_size, generations, mutation_probability):
        # Declaring Chromosomes
        population_1 = [Chromosome(np.random.permutation(self.num_genes)) for i in range(population_size)]

        # Storing Best Generation Data
        max_per_generation = np.zeros(generations)

        # Starting the iterations
        for generation in range(generations):
            population_2 = Selection.roulette(population_1)

            # Mutation
            for chromosome in population_2:
                if random.random() <= mutation_probability:
                    Mutation.shuffle_k_random_genes(chromosome.genes, 2)
                    chromosome.set_fitness()

            # Sorting population_3 to grab top 50%
            combined_population = sorted(population_1 + population_2)
            
            # Setting population_1 to copied population_3
            population_1 = copy.deepcopy(combined_population[:population_size])

            # Storing Best Fitness for that Generation
            max_per_generation[generation] = population_1[0].fitness
        
        # Returning Progress
        return max_per_generation


if __name__ == '__main__':
    # Instantiating TravelingSalesman class with file
    file_name = 'data/TSP1.csv'
    traveling_salesman = TravelingSalesman(file_name)

    # Declaring Parameters
    population_size = 100
    generations = 50
    mutation_probability = 0.01

    # Running the algorithm
    tic = time.perf_counter()
    max_per_generation = traveling_salesman.simple_genetic_algorithm(population_size, generations, mutation_probability)
    toc = time.perf_counter()
    print(max_per_generation)
    print(f'Time: {toc - tic} seconds.')
