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

genprg = projectpath.joinpath('gen').joinpath('closest_string.py')
lpfile = projectpath.joinpath('encoding').joinpath('closest_string.lp')
bruteprg = projectpath.joinpath('brute').joinpath('closest_string.py')
decodeprg = projectpath.joinpath('decode').joinpath('closest_string.py')

assert os.access(bruteprg, os.X_OK), f'cannot execute {bruteprg}'
assert os.access(genprg, os.X_OK), f'cannot execute {genprg}'
assert os.access(lpfile, os.R_OK), f'cannot read {lpfile}'
assert os.access(decodeprg, os.X_OK), f'cannot execute {decodeprg}'



# os.mkdir("/tmp/asp")
workDir="/tmp/asp"
if True:
# with tempfile.TemporaryDirectory(prefix='aspstr') as workDir:
	print(f'create tempdir at {workDir}')
	plaininputfilename = Path(workDir).joinpath('input.txt') 
	lpinputfilename = Path(workDir).joinpath('input.lp') 
	clingologfilename = Path(workDir).joinpath('clingo.log') 
	bruteoutputfilename = Path(workDir).joinpath('brute.log') 
	decodeoutputfilename = Path(workDir).joinpath('decode.log') 

	for _ in range(10):
	# generate text
		with open(plaininputfilename,'w') as out:
			textlength = random.randint(4, 10)
			textnum = random.randint(2, 5)
			for row in range(textnum):
				print(''.join((random.choice('abcd') for _ in range(textlength))), file=out)

	# generate clingo files

		with open(lpinputfilename,'w') as lpout:
			subprocess.check_call([genprg, plaininputfilename], stdout=lpout)

	# solve

		with open(clingologfilename,'w') as logout:
			stat = subprocess.run(['clingo', lpfile, lpinputfilename], stdout=logout)
		if stat.returncode != 30:
			die("call to clingo failed!")

	# decode
		with open(decodeoutputfilename,'w') as logout:
			subprocess.run([decodeprg, clingologfilename, plaininputfilename], stdout=logout)
		asp_result = extract_result(decodeoutputfilename)

	# brute force

		with open(bruteoutputfilename,'w') as bruteout:
			subprocess.check_call([bruteprg, plaininputfilename], stdout=bruteout)

		brute_result = extract_result(bruteoutputfilename)
		assert int(asp_result['distance']) == int(brute_result['distance'])
		# for line in open(bruteoutputfilename,'r').readlines():
		# 	if line.startswith('RESULT '):
		# 		brute_distance = int(re.sub(r'RESULT .*distance=([0-9]+) .*', r'\1', line))
		# 		assert brute_distance == asp_distance
		# 		break
