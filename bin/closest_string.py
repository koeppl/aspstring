#!/usr/bin/env python3

import tempfile
import sys
import os
import subprocess
from pathlib import Path

def die(err : str):
	print(err, file=sys.stderr)
	sys.exit(1)


from enum import Enum
class Flavor(Enum):
	cpm = 'cpm'
	default = ''
	def __str__(self):
		return self.value

projectpath = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()


import argparse

parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input text file", required=True)
parser.add_argument("--output", type=str, help="output stats file", default='')
parser.add_argument("--log", type=str, help="output clingo log file", default='')
parser.add_argument("--length", type=int, help="substring length (lambda)", default=0)
parser.add_argument("--flavor", help="which encoding version to run (cpm = conference version, without arguments: best version)", type=Flavor, choices=list(Flavor), default=Flavor.default)
args = parser.parse_args()

if args.flavor != Flavor.default:
	args.flavor = '_' + str(args.flavor)
else:
	args.flavor = ''

transprg = projectpath / ('translate') / ('text2lp.py')
lpfile = projectpath / ('encoding') / 'closest_string' / ('closest_string' + args.flavor + '.lp')
lpsubstringfile = projectpath / ('encoding') / 'closest_substring' / ('closest_substring' + args.flavor + '.lp')
decodeprg = projectpath / ('decode') / ('closest_string.py')

assert os.access(transprg, os.X_OK), f'cannot execute {transprg}'
assert os.access(lpfile, os.R_OK), f'cannot read {lpfile}'
assert os.access(lpsubstringfile, os.R_OK), f'cannot read {lpsubstringfile}'
assert os.access(decodeprg, os.X_OK), f'cannot execute {decodeprg}'

plaininputfilename = Path(args.input)
inputbasename = plaininputfilename.with_suffix('').name

# os.mkdir("/tmp/asp")
workDir=plaininputfilename.parent
lpinputfilename = workDir.joinpath(inputbasename + '.lp') 
clingologfilename = workDir.joinpath(inputbasename + '.clingo.log')  if args.log == '' else Path(args.log)
decodeoutputfilename = workDir.joinpath(inputbasename + '.decode.log') if args.output == '' else Path(args.output)

# generate clingo files
with open(lpinputfilename,'w') as lpout:
	subprocess.check_call([transprg, '--input', plaininputfilename], stdout=lpout)

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

