#!/usr/bin/env python3

import tempfile
import sys
import os
import subprocess
from pathlib import Path
import random
import re
import typing as t

def die(err : str):
	print(err, file=sys.stderr)
	sys.exit(1)

projectpath = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()

genprg = projectpath.joinpath('gen').joinpath('text2lp.py')
lpfile = projectpath.joinpath('encoding').joinpath('closest_string.lp')
lpsubstringfile = projectpath.joinpath('encoding').joinpath('closest_substring.lp')
decodeprg = projectpath.joinpath('decode').joinpath('closest_string.py')

assert os.access(genprg, os.X_OK), f'cannot execute {genprg}'
assert os.access(lpfile, os.R_OK), f'cannot read {lpfile}'
assert os.access(lpsubstringfile, os.R_OK), f'cannot read {lpsubstringfile}'
assert os.access(decodeprg, os.X_OK), f'cannot execute {decodeprg}'

import argparse

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input text file")
parser.add_argument("--output", type=str, help="output stats file", default='')
parser.add_argument("--log", type=str, help="output clingo log file", default='')
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
args = parser.parse_args()

plaininputfilename = Path(args.input)
inputbasename = plaininputfilename.with_suffix('').name

# os.mkdir("/tmp/asp")
workDir=plaininputfilename.parent
lpinputfilename = workDir.joinpath(inputbasename + '.lp') 
clingologfilename = workDir.joinpath(inputbasename + '.clingo.log')  if args.log == '' else Path(args.log)
decodeoutputfilename = workDir.joinpath(inputbasename + '.decode.log') if args.output == '' else Path(args.output)

# generate clingo files
with open(lpinputfilename,'w') as lpout:
	subprocess.check_call([genprg, plaininputfilename], stdout=lpout)

# solve
with open(clingologfilename,'w') as logout:
	if args.length == 0:
		stat = subprocess.run(['clingo', '--stats', lpfile, lpinputfilename], stdout=logout)
	else:
		with tempfile.NamedTemporaryFile(mode='w') as lplengthfile:
			lplengthfile.write(f'#const lambda={args.length}.')
			lplengthfile.flush()
			stat = subprocess.run(['clingo', '--stats', lpsubstringfile, lpinputfilename, lplengthfile.name], stdout=logout)
if stat.returncode != 30:
	die("call to clingo failed!")

# decode
with open(decodeoutputfilename,'w') as logout:
	subprocess.run([decodeprg, '--log', clingologfilename, '--input', plaininputfilename, '--length', str(args.length)], stdout=logout)

print(f'clingo logfile : {clingologfilename}')
print(f'logfile : {decodeoutputfilename}')
print(open(decodeoutputfilename, 'r').read())

