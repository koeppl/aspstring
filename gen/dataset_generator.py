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

alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

for n in [5, 10, 15, 20, 30]:
	for sigma in [2, 4, 8, 16, 32]:
		for m in [2, 4, 8, 16, 32, 64, 128]:
			for i in range(5):
				filename = folder / f's{sigma:02d}m{m:02d}n{n:03d}i{i}.txt'
				with open(filename, 'w') as out:
					for row in range(m):
						print(''.join((random.choice(alphabet[:sigma]) for _ in range(n))), file=out)

for n in [5, 10, 15, 20, 30, 40, 50, 100, 150, 200]:
	for sigma in [2, 4, 8, 16, 32]:
		for i in range(5):
			filename = folder / f'2s{sigma:02d}n{n:03d}i{i}.txt'
			with open(filename, 'w') as out:
				text = ''.join((random.choice(alphabet[:sigma]) for _ in range(n)))
				indices=list(range(len(text)))
				random.shuffle(indices)
				print(text, file=out)
				print(''.join(map(lambda x : text[indices[x]], range(len(text)))), file=out)
