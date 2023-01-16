#!/usr/bin/env python3

import argparse
from pathlib import Path 



def overlap(textA : str, textB : str) -> int:
	for length in range(min(len(textA), len(textB)), -1, -1):
		if textA.endswith(textB[:length]):
			return length
	return 0

parser = argparse.ArgumentParser(description='convert input text file into LP file required for shortest superstring encoding')
parser.add_argument("--input", type=str, help="input file", required=True)
args = parser.parse_args()


plaininputfilename = Path(args.input)
inputbasename = Path(plaininputfilename).with_suffix('').name

strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

m = len(strings)

for i, stri in enumerate(strings):
		for j, strj in enumerate(strings):
				if i == j:
					continue
				print(f'w({i},{j},{overlap(stri,strj)}).')

