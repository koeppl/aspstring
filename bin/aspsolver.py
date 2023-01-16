#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

def die(err : str):
	print(err, file=sys.stderr)
	sys.exit(1)

projectpath = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()


import argparse

parser = argparse.ArgumentParser(description='solve problem with ASP encoding')
parser.add_argument("--prg", type=str, help="which program to run (longest_common_subsequence, shortest_superstring, minimum_common_string_partition)", required=True)
parser.add_argument("--input", type=str, help="input text file", required=True)
parser.add_argument("--output", type=str, help="output stats file", default='')
parser.add_argument("--log", type=str, help="output clingo log file", default='')
args = parser.parse_args()

genprg = projectpath.joinpath('gen').joinpath('text2lp.py')
lpfile = projectpath.joinpath('encoding').joinpath(args.prg + '.lp')
decodeprg = projectpath.joinpath('decode').joinpath(args.prg + '.py')

assert os.access(genprg, os.X_OK), f'cannot execute {genprg}'
assert os.access(lpfile, os.R_OK), f'cannot read {lpfile}'
assert os.access(decodeprg, os.X_OK), f'cannot execute {decodeprg}'


# print('READ {plaininputfilename}')
plaininputfilename = Path(args.input)
assert os.access(plaininputfilename, os.R_OK), f'cannot read {plaininputfilename}'
inputbasename = plaininputfilename.with_suffix('').name

# os.mkdir("/tmp/asp")
workDir=plaininputfilename.parent
lpinputfilename = workDir.joinpath(inputbasename + '.lp') 
clingologfilename = workDir.joinpath(inputbasename + '.clingo.log')  if args.log == '' else Path(args.log)
decodeoutputfilename = workDir.joinpath(inputbasename + '.decode.log') if args.output == '' else Path(args.output)

# generate clingo files
with open(lpinputfilename,'w') as lpout:
	subprocess.check_call([genprg, '--input', plaininputfilename], stdout=lpout)

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

