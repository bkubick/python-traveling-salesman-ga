# coding: utf-8

import random
from typing import List, Optional, Union

import numpy as np


class Chromosome:
    def __init__(self, order, fitness):
        self.order = order
        self.fitness = fitness
