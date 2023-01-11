#!/usr/bin/env python3
import itertools
from tqdm import tqdm
import time
from pathlib import Path 

resultPrefix='RESULT type=csp method=brute '

def hamming_distance(textA, textB):
	assert len(textA) <= len(textB), f'{textA} must be at least as long as {textB}'
	return len([pos for pos in range(len(textA)) if textA[pos] != textB[pos]])

def max_hamming_distance(text, strings):
	return max(map(lambda s: hamming_distance(text, s), strings))

def local_hamming_distance(text : str, string : str):
	n = len(string)
	min_dist = len(text)
	for offset in range(n + 1 - len(text)):
		local_dist = hamming_distance(text, string[offset:])
		if local_dist < min_dist:
			min_dist = local_dist
	return min_dist

def max_local_hamming_distance(text, strings):
	return max(map(lambda s: local_hamming_distance(text, s), strings))

def closest_string(strings, quiet = False):
	alphabets=[]
	for i in range(len(strings[0])):
		distinct_chars = set(map(lambda x: strings[x][i], range(len(strings))))
		alphabets.append(distinct_chars)

	acc = 1; [acc := acc * len(alphabets[i]) for i in range(len(alphabets))]
	num_combinations = acc
	generator = itertools.product(*alphabets)

	best_text = strings[0]
	best_distance = len(best_text)

	start_time = time.time()
	with tqdm(generator, total=num_combinations, disable=quiet) as t:
		for text in t:
			distance = max_hamming_distance(text, strings)
			if distance < best_distance:
				t.set_description(f'{distance}')
				best_distance = distance
				best_text = text 
				if distance == 0: 
					break
	print(f'{resultPrefix} distance={best_distance} output={"".join(best_text)} seconds={time.time() - start_time} length=0 combinations={num_combinations}')

def closest_substring(strings, length : int, quiet : bool = False):
	alphabet = set(); [alphabet := alphabet.union(set(x)) for x in strings]

	generator = itertools.product(alphabet, repeat=length)
	num_combinations = pow(len(alphabet), length)

	best_text = strings[0]
	best_distance = len(best_text)

	start_time = time.time()
	with tqdm(generator, total=num_combinations, disable=quiet) as t:
		for text in t:
			text = ''.join(text)
			distance = max_local_hamming_distance(text, strings)
			if distance < best_distance:
				t.set_description(f'{distance}')
				best_distance = distance
				best_text = text 
				if distance == 0: 
					break
	print(f'{resultPrefix} distance={best_distance} output={"".join(best_text)} length={length} seconds={time.time() - start_time} combinations={num_combinations}')


import argparse

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
parser.add_argument("--quiet", action=argparse.BooleanOptionalAction, help="no progress bar", default=False)
args = parser.parse_args()

plaininputfilename = Path(args.input)
inputbasename = Path(plaininputfilename).with_suffix('').name
resultPrefix += f'input={inputbasename} '


strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

for x in range(len(strings)):
	assert len(strings[0]) == len(strings[x]), f'input string {x} has unequal length {len(strings[x])}'


if args.length == 0:
	closest_string(strings, args.quiet)
else:
	closest_substring(strings, args.length, args.quiet)



