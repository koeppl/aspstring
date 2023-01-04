#!/usr/bin/env python3
import sys
import itertools
from tqdm import tqdm


def hamming_distance(textA, textB):
	assert len(textA) <= len(textB), f'{textA} must be at least as long as {textB}'
	return len([pos for pos in range(len(textA)) if textA[pos] != textB[pos]])

def max_hamming_distance(text, strings):
	return max(map(lambda s: hamming_distance(text, s), strings))

strings=[]

with open(sys.argv[1], "r") as istream:
	strings = istream.read().splitlines() 

bestdistance = len(strings[0])
bestselection = ''

with tqdm(itertools.product(range(len(strings)), repeat=len(strings[0])), total=pow(len(strings), len(strings[0]))) as t:
	for selection in t:
		selected_text = ''.join(map(lambda pos: strings[selection[pos]][pos] ,range(len(selection))))
		distance = max_hamming_distance(selected_text, strings)
		if distance < bestdistance:
			t.set_description(f'{distance}')
			bestdistance = distance
			bestselection = selection
			if distance == 0: 
				break

bestselectedtext = ''.join(map(lambda pos: strings[bestselection[pos]][pos] ,range(len(bestselection))))
print(f'RESULT distance={bestdistance} bestselection={bestselection} closeststring={bestselectedtext}')
