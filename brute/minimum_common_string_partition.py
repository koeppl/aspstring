#!/usr/bin/env python3
import itertools
import time
from tqdm import tqdm
from pathlib import Path 

import argparse


# by David Vanderschel, https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning
def partitions(n, m = None):
	"""Partition n with a maximum part size of m. Yield non-increasing
	lists in decreasing lexicographic order. The default for m is
	effectively n, so the second argument is not needed to create the
	generator unless you do want to limit part sizes.
	"""
	if m is None or m >= n: yield [n]
	for f in range(n-1 if (m is None or m >= n) else m, 0, -1):
		for p in partitions(n-f, f): yield [f] + p


def distinguishing_partitions(n):
	for partition in partitions(n):
		processed = set()
		for el in itertools.permutations(partition):
			if el in processed:
				continue
			processed.add(el)
			yield el

def distinguishing_partition_assignment(n):
	for partition in distinguishing_partitions(n):
		for permutation in itertools.permutations(range(len(partition))):
			yield (partition, permutation)
								



parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--quiet", action=argparse.BooleanOptionalAction, help="no progress bar", default=False)
args = parser.parse_args()

plaininputfilename = Path(args.input)
inputbasename = Path(plaininputfilename).with_suffix('').name

strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

for x in range(len(strings)):
	assert len(strings[0]) == len(strings[x]), f'input string {x} has unequal length {len(strings[x])}'

import math

n = len(strings[0])
generator = distinguishing_partition_assignment(n)
num_combinations = 0
for z in range(1,n+1):
	num_combinations += math.comb(n, z) * math.factorial(z)

from collections import Counter
assert Counter(strings[0]) == Counter(strings[1]), "Parikh vector of both input strings mismatch!"

best_factorization = None

is_finished = False
start_time = time.time()
with tqdm(generator, total=num_combinations, disable=args.quiet) as t:
	for (lenS, pi) in t:
		assert len(pi) == len(lenS)

		if is_finished:
			break
		lenT = [0]*len(lenS)
		for x in range(len(lenS)):
			lenT[pi[x]] = lenS[x]

		posS = [0]
		posT = [0]
		for x in range(len(lenS)):
			posS.append(posS[-1] + lenS[x])
			posT.append(posT[-1] + lenT[x])

		# verbose=False
		# # if len(lenS) == 3: # and lenS == (2, 2, 2): # and lenT == [2,2,2]:
		# verbose = True
		# if verbose:
		# 	print(f"partS={lenS} posS={posS} partT={lenT} posT={posT} pi={pi}")
		is_equal = True
		for x in range(len(lenS)):
			y = pi[x]
			assert lenS[x] == lenT[y]
			# if verbose:
			# 	print(f'check {strings[0][posS[x]:posS[x]+lenS[x]]} <-> {strings[1][posT[y]:posT[y]+lenT[y]]}')
			if strings[0][posS[x]:posS[x]+lenS[x]] != strings[1][posT[y]:posT[y]+lenT[y]]:
				is_equal = False
		if not is_equal:
			continue
		factors = []
		for x in range(len(lenS)):
			factors.append( (posS[x], posT[x], lenS[x]) )
		if not best_factorization or len(factors) < len(best_factorization):
			best_factorization = factors
			t.set_description(f'{len(factors)}')

if best_factorization:
	factorstring = str(best_factorization).replace(' ', '')
	print(f'RESULT type=mcsp method=brute input={inputbasename} length={len(best_factorization)} seconds={time.time() - start_time} combinations={num_combinations} output="{factorstring}"')

