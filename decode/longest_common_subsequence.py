#!/usr/bin/env python3

import decode as dec
from collections import defaultdict

def decode(modelstring : str, strings):
	parsedic = dict() 
	optimal_value = None
	if modelstring.find('text(') != -1:
		return decode_cpm(modelstring, strings)

	for el in modelstring.split(' '):
		if el.startswith('optimal_value('):
			optimal_value = -dec.unary_function('optimal_value', el)
		if el.startswith('subsequence('):
			(l,i) = dec.binary_function('subsequence', el)
			parsedic[l] = i
	assert optimal_value != None
	if len(parsedic) == 0:
		assert optimal_value == 0
		return ''
	assert max(parsedic.keys())+1 == optimal_value, f"largest key {max(parsedic.keys())} is not in {optimal_value}"

	subsequence = [None] * optimal_value

	for i in range(optimal_value):
		subsequence[i] = chr(parsedic[i])

	for x in range(1,len(strings)):
		matched=0
		for i in range(len(strings[x])):
			if strings[x][i] == subsequence[matched]:
				matched += 1
			if matched == len(subsequence):
				break
		assert matched == len(subsequence), f"could only match {matched} characters, for the subsequence {subsequence}"
	return "".join(subsequence)

def decode_cpm(modelstring : str, strings):
	parsedic = defaultdict(dict)
	for el in modelstring.split(' '):
		if el.startswith('text('):
			(x,l,i) = dec.ternary_function('text', el)
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
