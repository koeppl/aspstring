#!/usr/bin/env python3
import itertools
from tqdm import tqdm

def hamming_distance(textA, textB):
	assert len(textA) <= len(textB), f'{textA} must be at least as long as {textB}'
	return len([pos for pos in range(len(textA)) if textA[pos] != textB[pos]])

def max_hamming_distance(text, strings):
	return max(map(lambda s: hamming_distance(text, s), strings))

def local_hamming_distance(text : str, string : str):
	n = len(string)
	min_dist = len(text)
	for offset in range(n - len(text)):
		local_dist = hamming_distance(text, string[offset:])
		if local_dist < min_dist:
			min_dist = local_dist
	return min_dist

def max_local_hamming_distance(text, strings):
	return max(map(lambda s: local_hamming_distance(text, s), strings))

def closest_string(strings):
	alphabets=[]
	for i in range(len(strings[0])):
		distinct_chars = set(map(lambda x: strings[x][i], range(len(strings))))
		alphabets.append(distinct_chars)

	acc = 1; [acc := acc * len(alphabets[i]) for i in range(len(alphabets))]
	num_combinations = acc
	generator = itertools.product(*alphabets)

	best_distance = len(strings[0])
	best_text = ''

	with tqdm(generator, total=num_combinations) as t:
		for text in t:
			distance = max_hamming_distance(text, strings)
			if distance < best_distance:
				t.set_description(f'{distance}')
				best_distance = distance
				best_text = text 
				if distance == 0: 
					break
	print(f'RESULT distance={best_distance} closeststring={"".join(best_text)}')

def closest_substring(strings, length : int):
	alphabet = set(); [alphabet := alphabet.union(set(x)) for x in strings]

	generator = itertools.product(alphabet, repeat=length)
	num_combinations = pow(len(alphabet), length)

	best_distance = len(strings[0])
	best_text = ''

	with tqdm(generator, total=num_combinations) as t:
		for text in t:
			text = ''.join(text)
			distance = max_local_hamming_distance(text, strings)
			if distance < best_distance:
				t.set_description(f'{distance}')
				best_distance = distance
				best_text = text 
				if distance == 0: 
					break
	print(f'RESULT distance={best_distance} closeststring={"".join(best_text)} length={length}')


import argparse

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
args = parser.parse_args()

plaininputfilename = args.input


strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

for x in range(len(strings)):
	assert len(strings[0]) == len(strings[x]), f'input string {x} has unequal length {len(strings[x])}'


if args.length == 0:
	closest_string(strings)
else:
	closest_substring(strings, args.length)



