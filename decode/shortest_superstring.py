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
	print(f'RESULT superstring={text} length={len(text)}')
	## check model
	return text 

import argparse

parser = argparse.ArgumentParser(description='decode closest string')
parser.add_argument("--log", type=str, help="log file")
parser.add_argument("--input", type=str, help="input file")
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
strings = open(plaininputfilename, 'r').read().splitlines()

decode(dec.extract_clingolog(clingologfilename), strings)

