#!/usr/bin/env python3

import tempfile
import sys
import os
import subprocess
from pathlib import Path
import random
import re
import typing as t

def split_keyvalueline(line: str) -> t.Mapping[str,str]:
	""" read a line of 'key=value' pairs separated by whitespace(s) into a dict """
	attrs=dict()
	while line.find('=') != -1:
		key = line[:line.find('=')]
		valuematch = re.match(r'^\S+', line[line.find('=')+1:])
		assert valuematch, 'invalid key/value line: %s' % line
		value = valuematch.group(0)
		line=line[len(key)+len(value)+1:]
		key = key.strip()
		value = value.strip()
		attrs[key] = value
	return attrs

def split_resultline(line: str) -> t.Mapping[str,str]:
	""" read a RESULT line and put the keyvalue pairs into a dict """
	return split_keyvalueline(line[len('RESULT '):].strip())

def extract_result(filename : Path):
	for line in open(filename,'r').readlines():
		if line.startswith('RESULT '):
			return split_resultline(line)


def die(err : str):
	print(err, file=sys.stderr)
	sys.exit(1)

projectpath = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()

aspprg = projectpath.joinpath('bin').joinpath('closest_string.py')
bruteprg = projectpath.joinpath('brute').joinpath('closest_string.py')

assert os.access(bruteprg, os.X_OK), f'cannot execute {bruteprg}'
assert os.access(aspprg, os.X_OK), f'cannot execute {aspprg}'

# for debugging:
# workDir="/tmp/asp"
# if True:
with tempfile.TemporaryDirectory(prefix='aspstr') as workDir:
	print(f'create tempdir at {workDir}')
	plaininputfilename = Path(workDir).joinpath('input.txt') 
	lpinputfilename = Path(workDir).joinpath('input.lp') 
	clingologfilename = Path(workDir).joinpath('clingo.log') 
	bruteoutputfilename = Path(workDir).joinpath('brute.log') 
	decodeoutputfilename = Path(workDir).joinpath('decode.log') 

	for length in range(4):
		for _ in range(10):
		# generate text
			with open(plaininputfilename,'w') as out:
				textlength = random.randint(4, 12)
				textnum = random.randint(2, 5)
				for row in range(textnum):
					print(''.join((random.choice('abcd') for _ in range(textlength))), file=out)

			subprocess.check_call([aspprg, '--input', plaininputfilename, '--output', decodeoutputfilename, '--log', clingologfilename, '--length', str(length)])
			asp_result = extract_result(decodeoutputfilename)

		# brute force
			with open(bruteoutputfilename,'w') as bruteout:
				subprocess.check_call([bruteprg, '--input', plaininputfilename, '--length', str(length)], stdout=bruteout)

			brute_result = extract_result(bruteoutputfilename)
			assert int(asp_result['distance']) == int(brute_result['distance'])
