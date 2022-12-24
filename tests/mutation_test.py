# coding: utf-8

import pytest

from src.mutation import Mutation

def test_select_k_unique_indices():
    k = 3
    max_index = 9
    min_index = 0

    unique_indices = Mutation._select_k_unique_indices(k=k, max_index=max_index, min_index=min_index)

    assert len(unique_indices) == k
    assert max(unique_indices) <= max_index
    assert min(unique_indices) >= min_index
    assert len(set(unique_indices)) == len(unique_indices)

def test_shuffle_or_shift():
    genes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random_indices = [0, 3, 5, 9]
    new_genes = [9, 1, 2, 0, 4, 3, 6, 7, 8, 5]

    Mutation._shuffle_or_shift(genes, random_indices)

    assert genes == new_genes
