import copy
import random
import time
from typing import List, Optional, Union

import numpy as np
from pandas import read_csv



class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = calculate_fitness(genes)
    
    def __lt__(self, other):
        return other.fitness > self.fitness
    
    def __gt__(self, other):
        return other.fitness < self.fitness

    def mutate_switch_two_genes(self):
        random_gene_0 = random_gene_1 = 1

        while random_gene_0 == random_gene_1:
            random_gene_0 =  random.randint(0, len(self.genes)-1)
            random_gene_1 =  random.randint(0, len(self.genes)-1)

        temp_gene = self.genes[random_gene_0]
        self.genes[random_gene_0] = self.genes[random_gene_1]
        self.genes[random_gene_1] = temp_gene
        self.fitness = calculate_fitness(self.genes)


def calculate_fitness(order):
    fitness = 0
    points = len(order)

    for i in range(points-1):
        m = int(order[i])
        n = int(order[i+1])
        fitness += fitness_matrix[m][n]

    m = int(order[points-1])
    n = int(order[0])
    fitness += fitness_matrix[m][n]
    return fitness


def roulette(population):
    # Fitnesses
    population_fitnesses = np.array([population[i].fitness for i in range(len(population))])
    total_fitness = np.sum(population_fitnesses)

    # Looking for the minimum value so a smaller fitness is a higher probability
    probabilities = 1 - np.array([population_fitness/total_fitness for population_fitness in population_fitnesses])

    # Calculating the cumulative Sum
    cumulative_sum = np.cumsum(probabilities)

    # Normalizing cumulative_sum
    normalized_cumulative_sum = cumulative_sum / cumulative_sum[-1]

    offspring = []
    # Grabbing indices of parents based on random_num falling inbetween bins
    for i in range(int(len(population)/2)):
        parent_1 = parent_2 = 0
        while parent_1 == parent_2:
            parent_1 = np.digitize(random.random(), normalized_cumulative_sum, right=True)
            parent_2 = np.digitize(random.random(), normalized_cumulative_sum, right=True)

        genes_1, genes_2 = double_point_crossover(population[parent_1].genes, population[parent_2].genes)
        offspring.extend([Chromosome(genes_1), Chromosome(genes_2)])

    return offspring


def double_point_crossover(genes_1, genes_2):
    gene_size = len(genes_1)

    # Declaring new_genes as numpy arrays
    new_genes_1 = -np.ones(gene_size)
    new_genes_2 = -np.ones(gene_size)

    # Calculating split point
    split_1 = split_2 = 0
    while split_1 == split_2:
        split_1 = random.randint(0,gene_size)
        split_2 = random.randint(0,gene_size)
    
    # Inserting elements
    if split_2 < split_1:
        temp = split_2
        split_2 = split_1
        split_1 = temp

    # Inserting Middle
    new_genes_1[split_1:split_2] = genes_2[split_1:split_2]
    new_genes_2[split_1:split_2] = genes_1[split_1:split_2]

    # Inserting Front
    for i in range(split_1):
        for j in range(gene_size):
            if genes_1[j] not in new_genes_1:
                new_genes_1[i] = genes_1[j]
                break
        for j in range(gene_size):
            if genes_2[j] not in new_genes_2:
                new_genes_2[i] = genes_2[j]
                break

    # Inserting Back
    for i in range(split_2, gene_size):
        for j in range(gene_size):
            if genes_1[j] not in new_genes_1:
                new_genes_1[i] = genes_1[j]
                break
        for j in range(gene_size):
            if genes_2[j] not in new_genes_2:
                new_genes_2[i] = genes_2[j]
                break
    return new_genes_1, new_genes_2


def initialize_matrix(data):
    v, w = np.split(data, [-1], axis=1)
    X = np.column_stack(np.repeat(v, len(v),  axis=1)).T
    Y = np.column_stack(np.repeat(w, len(w),  axis=1)).T
    return np.sqrt((X - X.T)**2 + (Y - Y.T)**2)


# Creating the fitness matrix
data = read_csv('data/TSP1.csv', header=None).to_numpy()
fitness_matrix = initialize_matrix(data)

# sizes
num_genes = len(data)
population_size = 10
generations = 10

# Declarations
mutation_probability = 0.01

# Declaring Chromosomes
population_1 = [Chromosome(np.random.permutation(num_genes)) for i in range(population_size)]

tic = time.perf_counter()
# Starting the iterations
for generation in range(generations):
    population_2 = roulette(population_1)

    # Mutation
    for chromosome in population_2:
        if random.random() <= mutation_probability:
            chromosome.mutate_switch_two_genes()

    # Sorting population_3 to grab top 50%
    combined_population = sorted(population_1 + population_2)
    
    # Setting population_1 to copied population_3
    population_1 = copy.deepcopy(combined_population[:population_size])

toc = time.perf_counter()
print(f'Time: {toc - tic} seconds.')
