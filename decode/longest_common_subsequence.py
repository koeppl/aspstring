#!/usr/bin/env python3

import decode as dec
from collections import defaultdict

def decode(modelstring : str, strings):
	parsedic = defaultdict(dict)
	for el in modelstring.split(' '):
		if el.startswith('c('):
			(x,l,i) = dec.ternary_function('c', el)
			parsedic[x][l] = i
	
	subsequence=[]
	assert 0 in parsedic
	for l in range(len(parsedic[0])):
		assert l in parsedic[0]
		assert parsedic[0][l] < len(strings[0])
		subsequence.append(strings[0][parsedic[0][l]])
		if l+1 < len(parsedic[0]):
			assert parsedic[0][l] < parsedic[0][l+1]
	for x in range(1,len(strings)):
		for l in range(len(subsequence)):
			i = parsedic[x][l]
			assert strings[x][i] == subsequence[l]
			if l+1 < len(parsedic[x]):
				assert parsedic[x][l] < parsedic[x][l+1]
	print(f'RESULT subsequence={"".join(subsequence)} length={len(subsequence)}')

import argparse

parser = argparse.ArgumentParser(description='longest common subsequence')
parser.add_argument("--log", type=str, help="log file")
parser.add_argument("--input", type=str, help="input file")
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
strings = open(plaininputfilename, 'r').read().splitlines()

decode(dec.extract_clingolog(clingologfilename), strings)

