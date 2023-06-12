#!/usr/bin/env python3

import decode as dec
import typing as t

def decode(modelstring : str, strings, outputlength : int) -> t.Tuple[str, int]:
	textdic = {}
	cost = {}	
	maxcost = None
	optimal_value = None
	for el in modelstring.split(' '):
		if el.startswith('optimal_value('):
			optimal_value = dec.unary_function('optimal_value', el)
		if el.startswith('mcost('):
			maxcost = dec.unary_function('mcost', el)
		elif el.startswith('t('):
			(key,val) = dec.binary_function('t', el)
			textdic[key] = val
		elif el.startswith('cost('):
			(key,val) = dec.binary_function('cost', el)
			cost[key] = val
	assert optimal_value != None
	if maxcost != None:
		assert optimal_value == maxcost

	
	if outputlength == 0:
		outputlength = len(strings[0])

	text = ['\0']*outputlength
	for pos in range(outputlength):
		assert pos in textdic, f'pos={pos} not in textdic={textdic}'
		text[pos] = chr(textdic[pos])
	# print(f'candidate closest substring : {"".join(text)}')
	# selected_text = ''.join(map(lambda pos: strings[text[pos]][pos] ,range(len(strings[0]))))
	for k in range(len(strings)):
		mincost = len(strings[0])
		for offset in range(len(strings[0])-outputlength+1):
			localcost = dec.hamming_distance(text, strings[k][offset:]) 
			if localcost < mincost:
				mincost = localcost
		assert mincost <= optimal_value, f'computed actual cost {mincost} is not bounded by the optimal cost {optimal_value}'
		if k in cost:
			assert cost[k] >= mincost, f'claimed cost[{k}] = {cost[k]} is lower than actual minimal cost {mincost}'
		else:
			cost[k] = mincost
	assert cost[max(cost, key=cost.get)] == optimal_value, f'maxel {max(cost, key=cost.get)} of {cost} is not {optimal_value}'
	## check model
	return ("".join(text), optimal_value)

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='decode closest string')
parser.add_argument("--log", type=str, help="log file", required=True)
parser.add_argument("--input", type=str, help="input file", required=True)
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
inputbasename = Path(plaininputfilename).with_suffix('').name
outputlength = args.length
strings = open(plaininputfilename, 'r').read().splitlines()

(text, maxcost) = decode(dec.extract_clingolog(clingologfilename), strings, outputlength)
stats = dec.extract_stats(clingologfilename)

print(f'RESULT type=csp method=asp output={"".join(text)} input={inputbasename} distance={maxcost} length={args.length} {stats}')
