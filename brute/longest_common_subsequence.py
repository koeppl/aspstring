#!/usr/bin/env python3
import itertools
from tqdm import tqdm
import time
from pathlib import Path 
import argparse

def is_subsequence(x : str, y : str):
	it = iter(y)
	return all(c in it for c in x)


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


n = len(strings[0])
generator = itertools.product([1,0], repeat=n)
num_combinations = 1<<n

best_length = 0
best_subsequence = ''

start_time = time.time()
with tqdm(generator, total=num_combinations, disable=args.quiet) as t:
	for selection in t:
		selected_chars = []
		for i in range(len(selection)):
			if selection[i] == 1:
				selected_chars.append(strings[0][i])
		selected_text = ''.join(selected_chars)
		if len(selected_text) < best_length:
			continue
		if not all(map(lambda i: is_subsequence(selected_text, strings[i]), range(1,len(strings)))):
			continue
		best_length = len(selected_text)
		best_subsequence = selected_text
		t.set_description(f'{best_length}')
print(f'RESULT type=lcs method=brute input={inputbasename} length={best_length} output="{best_subsequence}" seconds={time.time() - start_time} combinations={num_combinations}')
