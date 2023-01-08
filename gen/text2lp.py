#!/usr/bin/env python3

from typing import Dict
import sys

charno=0
with open(sys.argv[1], "r") as istream:
	strings = istream.read().splitlines()

stringno=0
for line in strings:
	charno=0
	for c in line:
		if not c.isprintable():
			continue
		print(f's({stringno},{charno}, {ord(c)}).')
		charno+=1
	stringno+=1

print(f'#const n={charno}.')
print(f'#const m={stringno}.')

majoritystring = [0]*len(strings[0])
for charno in range(len(strings[0])):
	characters = list(map(lambda x: strings[x][charno], range(len(strings))))
	statistics : Dict[str, int] = {c : characters.count(c) for c in set(characters)}
	character = max(statistics, key=statistics.get) # type: ignore (causes an error in old pyright)
	print(f'majority({charno}, {ord(character)}).')

