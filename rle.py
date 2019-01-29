# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 09:14:44 2019

@author: kpf
"""

from itertools import groupby, chain, repeat
from typing import Iterable


def encode(seq: Iterable) -> list:
    """Encodes sequence into a list of runs (RLE)"""
    return [(elm, len(tuple(grp))) for elm, grp in groupby(seq)]


def decode(rle: list) -> Iterable:
    """Decodes RLE-encoded sequence, returns iterator"""
    return chain.from_iterable(repeat(elm, cnt) for elm, cnt in rle)


def decode_list(rle: list) -> list:
    """Decodes RLE-encoded sequence into list"""
    return list(decode(rle))


def decode_tuple(rle: list) -> tuple:
    """Decodes RLE-encoded sequence into tuple"""
    return tuple(decode(rle))


def decode_str(rle: list) -> str:
    """Decodes RLE-encoded sequence into string. Will fail if elements are non-strings"""
    return ''.join(decode(rle))


# Example
# 
# src = [(1,2), (1,2), 'a', 'a', 3, 3, 5, 5, 5]
# encode(src)
# --> [((1, 2), 2), ('a', 2), (3, 2), (5, 3)]
# decode_list(encode(src))
# --> [(1, 2), (1, 2), 'a', 'a', 3, 3, 5, 5, 5]
# decode_list(encode(src)) == src
# --> True


# Timing it

from time import process_time


def time_encode(n_runs, inp):
    start = process_time()
    for i in range(n_runs):
        dummy_enc = encode(inp)
    print(f'Runtime encode: {process_time() - start}')


def time_decode(n_runs, inp):
    dummy_enc = encode(inp)
    
    start = process_time()
    for i in range(n_runs):
        dummy_dec = decode_list(dummy_enc)
    print(f'Runtime decode: {process_time() - start}')
