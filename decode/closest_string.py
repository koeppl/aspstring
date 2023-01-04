#!/usr/bin/env python3

import decode as d

def decode(modelstring : str, strings):
	f = {}
	cost = {}	
	maxcost = 0
	for el in modelstring.split(' '):
		if el.startswith('maxcost('):
			maxcost = d.unary_function('maxcost', el)
		elif el.startswith('f('):
			(key,val) = d.binary_function('f', el)
			f[val] = key
		elif el.startswith('cost('):
			(key,val) = d.binary_function('cost', el)
			cost[key] = val

	for pos in range(len(strings[0])):
		assert pos in f, f'pos={pos} not in f={f}'
		assert f[pos] < len(strings)
	selected_text = ''.join(map(lambda pos: strings[f[pos]][pos] ,range(len(strings[0]))))
	for k in range(len(strings)):
		assert k in cost
		assert d.hamming_distance(selected_text, strings[k]) == cost[k]
		assert cost[max(cost, key=cost.get)] == maxcost, f'maxel {max(cost, key=cost.get)} of {cost} is not {maxcost}'
	print(f"RESULT closeststring={selected_text} distance={maxcost}")
	## check model
	return maxcost

import sys

clingologfilename = sys.argv[1]
plaininputfilename = sys.argv[2]
strings = open(plaininputfilename, 'r').read().splitlines()

decode(d.extract_clingolog(clingologfilename), strings)

