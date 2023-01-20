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

prgname = 'shortest_superstring'

aspprg = projectpath.joinpath('bin').joinpath(prgname + '.py')
bruteprg = projectpath.joinpath('brute').joinpath(prgname + '.py')

assert os.access(bruteprg, os.X_OK), f'cannot execute {bruteprg}'
assert os.access(aspprg, os.X_OK), f'cannot execute {aspprg}'

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
		# generate text
		with open(plaininputfilename,'w') as out:
				textlength = random.randint(4, 12)
				textnum = random.randint(2, 5)
				for row in range(textnum):
					print(''.join((random.choice('abcd') for _ in range(textlength))), file=out)

		try:
			subprocess.check_call([aspprg, '--input', plaininputfilename, '--output', decodeoutputfilename, '--log', clingologfilename ])
		except subprocess.CalledProcessError as e:
			print('CALL' + ' '.join(map(str, e.cmd)))
			raise(e)
		asp_result = common.extract_result(decodeoutputfilename)

	# brute force
		with open(bruteoutputfilename,'w') as bruteout:
			subprocess.check_call([bruteprg, '--input', plaininputfilename], stdout=bruteout)

		brute_result = common.extract_result(bruteoutputfilename)
		assert int(asp_result['length']) == int(brute_result['length'])
