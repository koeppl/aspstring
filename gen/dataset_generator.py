#!/usr/bin/env python3

import argparse
import random
from pathlib import Path 


parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--folder", type=str, help="output directory", required=True)
parser.add_argument("--seed", type=int, help="output directory", default='0')
args = parser.parse_args()

random.seed(args.seed)

folder = Path(args.folder)
folder.mkdir(exist_ok=True)

mcsp_folder = (folder / 'mcsp')
scs_folder = (folder / 'scs')
lcs_folder = (folder / 'lcs')
csp_folder = (folder / 'csp')

mcsp_folder.mkdir(exist_ok=True)
scs_folder.mkdir(exist_ok=True)
lcs_folder.mkdir(exist_ok=True)
csp_folder.mkdir(exist_ok=True)

alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

for n in range(5,11):
	for sigma in range(4,9):
		for m in range(5,12):
			for i in range(3):
				filename = csp_folder / f's{sigma:02d}m{m:02d}n{n:03d}i{i}.txt'
				with open(filename, 'w') as out:
					for row in range(m):
						print(''.join((random.choice(alphabet[:sigma]) for _ in range(n))), file=out)

for n in range(18, 24):
	for sigma in range(2,9):
		for m in range(5,12):
			for i in range(3):
				filename = lcs_folder / f's{sigma:02d}m{m:02d}n{n:03d}i{i}.txt'
				with open(filename, 'w') as out:
					for row in range(m):
						print(''.join((random.choice(alphabet[:sigma]) for _ in range(n))), file=out)

n=8
sigma=2
for m in range(10,13):
	for i in range(3):
		filename = scs_folder / f's{sigma:02d}m{m:02d}n{n:03d}i{i}.txt'
		with open(filename, 'w') as out:
			for row in range(m):
				print(''.join((random.choice(alphabet[:sigma]) for _ in range(n))), file=out)


for n in range(8,11):
	for sigma in range(2,4):
		for i in range(3):
			filename = mcsp_folder / f'2s{sigma:02d}n{n:03d}i{i}.txt'
			with open(filename, 'w') as out:
				text = ''.join((random.choice(alphabet[:sigma]) for _ in range(n)))
				indices=list(range(len(text)))
				random.shuffle(indices)
				print(text, file=out)
				print(''.join(map(lambda x : text[indices[x]], range(len(text)))), file=out)
