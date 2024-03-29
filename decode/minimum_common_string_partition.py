#!/usr/bin/env python3

import decode as dec

def decode(modelstring : str, strings):
	ppos = []
	qpos = []
	ref = {}
	for el in modelstring.split(' '):
		if el.startswith('p('):
			ppos.append(dec.unary_function('p', el))
		if el.startswith('q('):
			qpos.append(dec.unary_function('q', el))
		if el.startswith('ref('):
			(key,val) = dec.binary_function('ref', el)
			ref[key] = val
	ppos.sort()
	qpos.sort()

	if len(ppos) == 0:
		ppos = [0]
		qpos = [0]
		for p in ref:
			q = ref[p]
			if p == 0 and q > 0:
					qpos.append(q)
			if q == 0 and p > 0:
					ppos.append(p)
			if p == 0 or q == 0:
				continue
			prevq = ref[p-1]
			if prevq != q-1:
				ppos.append(p)
				qpos.append(q)
		ppos = sorted(list(set(ppos)))
		qpos = sorted(list(set(qpos)))


		startpos = sorted(ref.keys())

	assert len(ppos) == len(qpos), f'list of starting positions mismatch in length: {ppos} <-> {qpos}'
	# assert len(ref.values()) == len(qpos)

	n = len(strings[0])
	z = len(ppos)

	factors=[]
	for p_it in range(z):
		assert ppos[p_it] in ref
		assert ref[ppos[p_it]] in qpos
		q_it = qpos.index(ref[ppos[p_it]])
		plength = ppos[p_it+1]-ppos[p_it] if p_it+1 < z else n-ppos[p_it]
		qlength = qpos[q_it+1]-qpos[q_it] if q_it+1 < z else n-qpos[q_it]
		assert plength == qlength, f'plen = {plength} != qlen = {qlength} for factor with p={ppos[p_it]} and q={qpos[q_it]}'
		for l in range(plength):
			assert strings[0][ppos[p_it]+l] == strings[1][qpos[q_it]+l], f'strings mismatch at positions {ppos[p_it]+l} and {qpos[q_it]+l} with length l={l} : {strings[0][ppos[p_it]+l]} and {strings[1][qpos[q_it]+l]}'
		factors.append( (ppos[p_it], qpos[q_it], plength))

	return factors

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='decode common partition')
parser.add_argument("--log", type=str, help="log file", required=True)
parser.add_argument("--input", type=str, help="input file", required=True)
args = parser.parse_args()


clingologfilename = args.log
plaininputfilename = args.input
inputbasename = Path(plaininputfilename).with_suffix('').name
strings = open(plaininputfilename, 'r').read().splitlines()

factors = decode(dec.extract_clingolog(clingologfilename), strings)
stats = dec.extract_stats(clingologfilename)

factorstring = str(factors).replace(' ', '')

print(f'RESULT type=mcsp method=asp input={inputbasename} length={len(factors)} output="{factorstring}" {stats}')
