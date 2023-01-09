#!/usr/bin/env python3

import decode as dec
import typing as t

def decode(modelstring : str, strings, outputlength : int) -> t.Tuple[str, int]:
	textdic = {}
	cost = {}	
	maxcost = 0
	for el in modelstring.split(' '):
		if el.startswith('maxcost('):
			maxcost = dec.unary_function('maxcost', el)
		elif el.startswith('t('):
			(key,val) = dec.binary_function('t', el)
			textdic[key] = val
		elif el.startswith('cost('):
			(key,val) = dec.binary_function('cost', el)
			cost[key] = val
	
	if outputlength == 0:
		outputlength = len(strings[0])

	text = ['\0']*outputlength
	for pos in range(outputlength):
		assert pos in textdic, f'pos={pos} not in textdic={textdic}'
		text[pos] = chr(textdic[pos])
	# print(f'candidate closest substring : {"".join(text)}')
	# selected_text = ''.join(map(lambda pos: strings[text[pos]][pos] ,range(len(strings[0]))))
	for k in range(len(strings)):
		assert k in cost
		mincost = len(strings[0])
		for offset in range(len(strings[0])-outputlength+1):
			localcost = dec.hamming_distance(text, strings[k][offset:]) 
			if localcost < mincost:
				mincost = localcost
		assert cost[k] >= mincost, f'claimed cost[{k}] = {cost[k]} is lower than actual minimal cost {mincost}'
		assert cost[max(cost, key=cost.get)] == maxcost, f'maxel {max(cost, key=cost.get)} of {cost} is not {maxcost}'
	## check model
	return ("".join(text), maxcost)

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='decode closest string')
parser.add_argument("--log", type=str, help="log file")
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
inputbasename = Path(plaininputfilename).with_suffix('').name
outputlength = args.length
strings = open(plaininputfilename, 'r').read().splitlines()

(text, maxcost) = decode(dec.extract_clingolog(clingologfilename), strings, outputlength)
(total_secs, solve_secs) = dec.extract_time(clingologfilename)

print(f'RESULT closeststring={"".join(text)} input={inputbasename} distance={maxcost} solve_seconds={solve_secs} seconds={total_secs} length={args.length}')
