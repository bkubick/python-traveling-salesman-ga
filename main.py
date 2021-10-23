# coding: utf-8
import time

from src.genetic_algorithm import TravelingSalesman

if __name__ == '__main__':
    # Instantiating TravelingSalesman class with file
    file_name = 'data/TSP1.csv'
    traveling_salesman = TravelingSalesman(file_name)

    # Declaring Parameters
    population_size = 10
    generations = 20
    mutation_probability = 0.01

    # Running the algorithm
    tic = time.perf_counter()
    max_per_generation = traveling_salesman.simple_genetic_algorithm(population_size, generations, mutation_probability)
    toc = time.perf_counter()
    print(max_per_generation)
    print(f'Time: {toc - tic} seconds.')
