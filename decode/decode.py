import re
import typing as t

def unary_function(fnTime : str, coding :str):
	return int(re.sub(fnTime + r'\(([0-9]+)\)', r'\1', coding))
def binary_function(fnTime : str, coding :str):
	return tuple(map(lambda x: int(x), re.sub(fnTime + r'\(([0-9]+),([0-9]+)\)', r'\1 \2', coding).split(' ')))

def ternary_function(fnTime : str, coding :str):
	return tuple(map(lambda x: int(x), re.sub(fnTime + r'\(([0-9]+),([0-9]+),([0-9]+)\)', r'\1 \2 \3', coding).split(' ')))

def hamming_distance(textA, textB):
	assert len(textA) <= len(textB), f'{textA} must be at least as long as {textB}'
	return len([pos for pos in range(len(textA)) if textA[pos] != textB[pos]])


def extract_clingolog(clingologfilename : str):
		lines = open(clingologfilename,'r').readlines()
		for row, line in enumerate(open(clingologfilename,'r').readlines()):
			if line.startswith('OPTIMUM FOUND'):
				assert row > 2
				return lines[row-2]
		return ''

fnTime='Time '
flreg=r'(\d+\.?\d+)'
timeRegex = fnTime + r'\s*:\s*' + flreg + r's.* \(Solving: ' + flreg + r's.*'

def extract_stats(clingologfilename : str) -> str:
	variables = 0
	rules = 0
	constraints = 0
	seconds = 0.0
	solve_seconds = 0.0
	for line in open(clingologfilename,'r').readlines():
		if line.startswith('Variables '):
			variables = int(re.sub(r'Variables\s*:\s*([0-9]+).*', r'\1', line))
		elif line.startswith('Constraints '):
			constraints = int(re.sub(r'Constraints\s*:\s*([0-9]+).*', r'\1', line))
		elif line.startswith('Rules '):
			rules = int(re.sub(r'Rules\s*:\s*([0-9]+).*', r'\1', line))
		elif line.startswith(fnTime):
			match = re.sub(timeRegex, r'\1 \2', line)
			(seconds, solve_seconds) = tuple(map(lambda x: float(x), match.split(' ')))
	return f'variables={variables} rules={rules} constraints={constraints} seconds={seconds} solve_seconds={solve_seconds}'
