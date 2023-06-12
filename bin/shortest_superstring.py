#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

def die(err : str):
	print(err, file=sys.stderr)
	sys.exit(1)

projectpath = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()

from enum import Enum
class Flavor(Enum):
	cpm = 'cpm'
	default = ''
	def __str__(self):
		return self.value

import argparse

parser = argparse.ArgumentParser(description='solve problem with ASP encoding')
parser.add_argument("--input", type=str, help="input text file", required=True)
parser.add_argument("--output", type=str, help="output stats file", default='')
parser.add_argument("--flavor", help="which encoding version to run (cpm = conference version, without arguments: best version)", type=Flavor, choices=list(Flavor), default=Flavor.default)
parser.add_argument("--log", type=str, help="output clingo log file", default='')
args = parser.parse_args()

if args.flavor != Flavor.default:
	args.flavor = '_' + str(args.flavor)
else:
	args.flavor = ''

prgname = 'shortest_superstring'
transprg = projectpath / ('translate') / (prgname + '.py')
lpfile = projectpath / ('encoding') / prgname / (prgname + args.flavor + '.lp')
decodeprg = projectpath / ('decode') / (prgname + '.py')

assert os.access(transprg, os.X_OK), f'cannot execute {transprg}'
assert os.access(lpfile, os.R_OK), f'cannot read {lpfile}'
assert os.access(decodeprg, os.X_OK), f'cannot execute {decodeprg}'


# print('READ {plaininputfilename}')
plaininputfilename = Path(args.input)
assert os.access(plaininputfilename, os.R_OK), f'cannot read {plaininputfilename}'
inputbasename = plaininputfilename.with_suffix('').name

# os.mkdir("/tmp/asp")
workDir=plaininputfilename.parent
lpinputfilename = workDir.joinpath(inputbasename + '.scs.lp') 
clingologfilename = workDir.joinpath(inputbasename + '.clingo.log')  if args.log == '' else Path(args.log)
decodeoutputfilename = workDir.joinpath(inputbasename + '.decode.log') if args.output == '' else Path(args.output)

# generate clingo files
with open(lpinputfilename,'w') as lpout:
	subprocess.check_call([transprg, '--input', plaininputfilename], stdout=lpout)

# solve
with open(clingologfilename,'w') as logout:
	stat = subprocess.run(['clingo', '--stats', lpfile, lpinputfilename], stdout=logout)
if stat.returncode != 30:
	die(f'call to clingo failed: clingo {lpfile} {lpinputfilename} !')

# decode
with open(decodeoutputfilename,'w') as logout:
	subprocess.run([decodeprg, '--log', clingologfilename, '--input', plaininputfilename], stdout=logout)

print(f'clingo logfile : {clingologfilename}')
print(f'logfile : {decodeoutputfilename}')
print(open(decodeoutputfilename, 'r').read())

