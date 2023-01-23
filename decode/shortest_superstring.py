#!/usr/bin/env python3

import decode as dec

def overlap(textA : str, textB : str) -> int:
	for length in range(min(len(textA), len(textB)), -1, -1):
		if textA.endswith(textB[:length]):
			return length
	return 0

def decode(modelstring : str, strings):
	textdic = {}
	startnode = -1
	for el in modelstring.split(' '):
		if el.startswith('cycle('):
			(key,val) = dec.binary_function('cycle', el)
			textdic[key] = val
		if el.startswith('start('):
			startnode = dec.unary_function('start', el)
	assert startnode != -1

	# print(f"textdic={textdic}, startnode={startnode}")
	cycle_array = [startnode]
	while True:
		next_val = textdic[cycle_array[-1]]
		if next_val == cycle_array[0]:
			break
		cycle_array.append(textdic[cycle_array[-1]])
	# print(f"cycle_array={cycle_array}")
	
	assert 0 in textdic, f'pos=0 not in textdic={textdic}'
	text = list(strings[cycle_array[0]])

	for pos in range(1,len(cycle_array)):
		length = overlap(strings[cycle_array[pos-1]], strings[cycle_array[pos]])
		text.append(strings[cycle_array[pos]][length:])
	text = ''.join(text)
	for string in strings:
		assert string in text, f"string {string} not in superstring {text}"
	return text 

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='decode closest string')
parser.add_argument("--log", type=str, help="log file", required=True)
parser.add_argument("--input", type=str, help="input file", required=True)
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
inputbasename = Path(plaininputfilename).with_suffix('').name

strings = open(plaininputfilename, 'r').read().splitlines()
stats = dec.extract_stats(clingologfilename)

superstring = decode(dec.extract_clingolog(clingologfilename), strings)
print(f'RESULT type=scs method=asp input={inputbasename} output={superstring} length={len(superstring)} {stats}')
