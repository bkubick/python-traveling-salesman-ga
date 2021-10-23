# coding: utf-8

import copy
import random

import numpy as np
from pandas import read_csv

from src.chromosome import Chromosome
from src.fitness import Fitness
from src.selection import Selection


class TravelingSalesman:
    def __init__(self, file_name):
        data = read_csv(file_name, header=None).to_numpy()
        Fitness.initialize_fitness_matrix(data)

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
                    chromosome.mutate_switch_two_genes()

            # Sorting population_3 to grab top 50%
            combined_population = sorted(population_1 + population_2)
            
            # Setting population_1 to copied population_3
            population_1 = copy.deepcopy(combined_population[:population_size])

            # Storing Best Fitness for that Generation
            max_per_generation[generation] = population_1[0].fitness
        
        # Returning Progress
        return max_per_generation
