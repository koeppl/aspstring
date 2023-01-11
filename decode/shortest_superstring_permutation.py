#!/usr/bin/env python3

import decode as dec

def decode(modelstring : str, strings):
	textdic = {}
	for el in modelstring.split(' '):
		if el.startswith('t('):
			(key,val) = dec.binary_function('t', el)
			if val > 0:
				textdic[key] = val

	text = ['\0']*len(textdic)
	for pos in range(len(textdic)):
		assert pos in textdic, f'pos={pos} not in textdic={textdic}'
		text[pos] = chr(textdic[pos])
	# selected_text = ''.join(map(lambda pos: strings[text[pos]][pos] ,range(len(strings[0]))))
	text = ''.join(text)
	for string in strings:
		assert string in text
	## check model
	return text 

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='decode closest string')
parser.add_argument("--log", type=str, help="log file")
parser.add_argument("--input", type=str, help="input file")
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
inputbasename = Path(plaininputfilename).with_suffix('').name

strings = open(plaininputfilename, 'r').read().splitlines()
stats = dec.extract_stats(clingologfilename)

superstring = decode(dec.extract_clingolog(clingologfilename), strings)
print(f'RESULT type=scs method=asp input={inputbasename} output={superstring} length={len(superstring)} {stats}')
