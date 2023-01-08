#!/usr/bin/env python3
## works with the files of https://github.com/jeanpttorres/dssp by stripping away the header

import sys
import re

lines = open(sys.argv[1], 'r').read().splitlines()
assert len(lines) > 5
sigma = int(lines[0])
(m1,m2) = map(lambda x: int(x), re.sub(r'([0-9]+) ([0-9]+)', r'\1 \2', lines[1]).split(' '))
m = m1 + m2
n = int(lines[2])

with open(re.sub(r'\.dssp$', '.txt', sys.argv[1]),'w') as os:
	for line in lines[sigma+4:]:
		print(line, file=os)



