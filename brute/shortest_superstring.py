#!/usr/bin/env python3
import itertools
import time
from tqdm import tqdm
import math

import argparse

def overlap(first, second):
	for length in range(min(len(first),len(second)),0,-1):
		if first[-length:] == second[:length]:
			return length
	return 0

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
args = parser.parse_args()

plaininputfilename = args.input

strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

m = len(strings)
n = len(strings[0])

generator = itertools.permutations(range(m))
num_combinations = math.factorial(m)


best_superstring = ''.join(strings)
best_length = len(best_superstring)
for string in strings:
	assert string in best_superstring

start_time = time.time()
with tqdm(generator, total=num_combinations) as t:
	for pi in t:
		assert len(pi) == m
		superstring = strings[pi[0]]
		for x in range(1, len(pi)):
			if strings[pi[x]] in superstring:
				continue
			length = overlap(superstring, strings[pi[x]])
			superstring += strings[pi[x]][length:]
		if len(superstring) < best_length:
			best_length = len(superstring)
			best_superstring = superstring
			t.set_description(f'{best_length}')
			for string in strings:
				assert string in best_superstring
print(f'RESULT length={best_length} superstring={best_superstring} seconds={time.time() - start_time}')




