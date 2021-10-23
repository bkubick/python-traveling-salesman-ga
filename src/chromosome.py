# coding: utf-8

import copy
import random

class Chromosome:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness
    
    def __lt__(self, other):
        return other.fitness > self.fitness
    
    def __gt__(self, other):
        return other.fitness < self.fitness

    def __eq__(self, other):
        return other.fitness == self.fitness
