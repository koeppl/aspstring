#!/usr/bin/env python3

import tempfile
import sys
import os
import subprocess
from pathlib import Path
import random
import common

def die(err : str):
	print(err, file=sys.stderr)
	sys.exit(1)

projectpath = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()

aspprg = projectpath.joinpath('bin').joinpath('aspsolver.py')
assert os.access(aspprg, os.X_OK), f'cannot execute {aspprg}'

prg_names = ['longest_common_subsequence', 'shortest_superstring_permutation', 'minimum_common_string_partition']
measures = ['length', 'length', 'length']

brute_prgs = []
for prg_name in prg_names:
	brute_prg = projectpath.joinpath('brute').joinpath(prg_name + '.py')
	assert os.access(brute_prg, os.X_OK), f'cannot execute {brute_prg}'
	brute_prgs.append(brute_prg)
# for program_it in range(len(prg_names)):



# for debugging:
# workDir="/tmp/asp"
# if True:
with tempfile.TemporaryDirectory(prefix='aspstr') as workDir:
	print(f'create tempdir at {workDir}')
	plaininputfilename = Path(workDir).joinpath('input.txt') 
	lpinputfilename = Path(workDir).joinpath('input.lp') 
	clingologfilename = Path(workDir).joinpath('clingo.log') 
	bruteoutputfilename = Path(workDir).joinpath('brute.log') 
	decodeoutputfilename = Path(workDir).joinpath('decode.log') 

	for _ in range(15):
		for program_it in range(len(prg_names)):
			# generate text
			with open(plaininputfilename,'w') as out:
				if prg_names[program_it] == 'minimum_common_string_partition':
					textlength = random.randint(4, 8)
					text = ''.join((random.choice('abcd') for _ in range(textlength)))
					indices=list(range(len(text)))
					random.shuffle(indices)
					print(text, file=out)
					print(''.join(map(lambda x : text[indices[x]], range(len(text)))), file=out)
				else:
					textlength = random.randint(4, 12)
					textnum = random.randint(2, 5)
					for row in range(textnum):
						print(''.join((random.choice('abcd') for _ in range(textlength))), file=out)

			try:
				subprocess.check_call([aspprg, '--input', plaininputfilename, '--output', decodeoutputfilename, '--log', clingologfilename, '--prg', prg_names[program_it] ])
			except subprocess.CalledProcessError as e:
				print('CALL' + ' '.join(map(str, e.cmd)))
				raise(e)
			asp_result = common.extract_result(decodeoutputfilename)

		# brute force
			with open(bruteoutputfilename,'w') as bruteout:
				subprocess.check_call([brute_prgs[program_it], '--input', plaininputfilename], stdout=bruteout)

			brute_result = common.extract_result(bruteoutputfilename)
			try:
				assert int(asp_result[measures[program_it]]) == int(brute_result[measures[program_it]]), f'ASP value: {asp_result[measures[program_it]]}, brute value: {brute_result[measures[program_it]]} for measure {measures[program_it]} with program {prg_names[program_it]}'
			except KeyError as e:
				print(f'error at evaluating {prg_names[program_it]}')
				print(f'asp_result: {asp_result}')
				print(f'brute_result: {brute_result}')

				raise e

				
