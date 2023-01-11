#!/usr/bin/env python3
import itertools
import time
from tqdm import tqdm
import math
from pathlib import Path 

import argparse

def overlap(first, second):
	for length in range(min(len(first),len(second)),0,-1):
		if first[-length:] == second[:length]:
			return length
	return 0

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--quiet", action=argparse.BooleanOptionalAction, help="no progress bar", default=False)
args = parser.parse_args()

plaininputfilename = Path(args.input)
inputbasename = Path(plaininputfilename).with_suffix('').name

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
with tqdm(generator, total=num_combinations, disable=args.quiet) as t:
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
print(f'RESULT type=scs method=brutepermut input={inputbasename} length={best_length} output={best_superstring} seconds={time.time() - start_time} combinations={num_combinations}')




