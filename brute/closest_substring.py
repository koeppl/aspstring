#!/usr/bin/env python3
import itertools
from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
args = parser.parse_args()

plaininputfilename = args.input

def hamming_distance(textA, textB):
	assert len(textA) <= len(textB), f'{textA} must be at least as long as {textB}'
	return len([pos for pos in range(len(textA)) if textA[pos] != textB[pos]])

def max_hamming_distance(text, strings):
	return max(map(lambda s: hamming_distance(text, s), strings))

strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

for x in range(len(strings)):
	assert len(strings[0]) == len(strings[x]), f'input string {x} has unequal length {len(strings[x])}'


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

# bestselectedtext = ''.join(map(lambda pos: strings[bestselection[pos]][pos] ,range(len(bestselection))))
print(f'RESULT distance={best_distance} closeststring={"".join(best_text)}')
