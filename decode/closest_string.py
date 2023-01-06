#!/usr/bin/env python3

import decode as dec

def decode(modelstring : str, strings, outputlength : int):
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
	# selected_text = ''.join(map(lambda pos: strings[text[pos]][pos] ,range(len(strings[0]))))
	for k in range(len(strings)):
		assert k in cost
		mincost = len(strings[0])
		for offset in range(len(strings[0])-outputlength+1):
			localcost = dec.hamming_distance(text, strings[k][offset:]) 
			if localcost < mincost:
				mincost = localcost
		assert cost[k] == mincost, f'cost[{k}] = {cost[k]} does not match with computed cost {mincost}'
		assert cost[max(cost, key=cost.get)] == maxcost, f'maxel {max(cost, key=cost.get)} of {cost} is not {maxcost}'
	print(f'RESULT closeststring={"".join(text)} distance={maxcost}')
	## check model
	return maxcost

import argparse

parser = argparse.ArgumentParser(description='decode closest string')
parser.add_argument("--log", type=str, help="log file")
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
outputlength = args.length
strings = open(plaininputfilename, 'r').read().splitlines()

decode(dec.extract_clingolog(clingologfilename), strings, outputlength)

