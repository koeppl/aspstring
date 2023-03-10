#!/usr/bin/env python3

import decode as dec
from collections import defaultdict

def decode(modelstring : str, strings):
	parsedic = defaultdict(dict)
	for el in modelstring.split(' '):
		if el.startswith('c('):
			(x,l,i) = dec.ternary_function('c', el)
			parsedic[x][l] = i
	
	if len(parsedic) == 0: #no solution
		return ""
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
	return "".join(subsequence)

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='longest common subsequence')
parser.add_argument("--log", type=str, help="log file", required=True)
parser.add_argument("--input", type=str, help="input file", required=True)
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
inputbasename = Path(plaininputfilename).with_suffix('').name
strings = open(plaininputfilename, 'r').read().splitlines()

subsequence = decode(dec.extract_clingolog(clingologfilename), strings)
stats = dec.extract_stats(clingologfilename)

print(f'RESULT type=lcs method=asp input={inputbasename} output="{"".join(subsequence)}" length={len(subsequence)} {stats}')
