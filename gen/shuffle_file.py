#!/usr/bin/env python3

import argparse
import random


parser = argparse.ArgumentParser(description='generate jumbled samples from given prefix')
parser.add_argument("--input", type=str, help="input text file whose prefix to parse", required=True)
parser.add_argument("--output", type=str, help="output text file", required=True)
parser.add_argument("--prefix", type=int, help="prefix length (=n)", default=10)
parser.add_argument("--number", type=int, help="number of strings (=m)", default=2)
parser.add_argument("--seed", type=int, help="seed for random generator")
args = parser.parse_args()

if args.seed:
	random.seed(args.seed)

text = open(args.input,'r').read().replace('\n','')
if args.prefix > 0:
	text = text[:args.prefix]


with open(args.output,'w') as outfile:
	print(text, file=outfile)
	for seq in range(args.number-1):
		indices = list(range(len(text)))
		random.shuffle(indices)
		print(''.join(map(lambda x: text[x], indices)), file=outfile)
