#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='stats about a file')
parser.add_argument("--input", type=str, help="input text file", required=True)
args = parser.parse_args()

plaininputfilename = Path(args.input)
baseinputname = os.path.basename(plaininputfilename)
assert os.access(plaininputfilename, os.R_OK), f'cannot read {plaininputfilename}'
with open(plaininputfilename, 'r') as infile:
	strings = infile.read().splitlines()
	alphabet = set(); [alphabet := alphabet.union(set(x)) for x in strings]
	print(f'RESULT type=fileinfo input={baseinputname} n={len(strings[0])} m={len(strings)} sigma={len(alphabet)}')


