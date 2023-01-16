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


def extract_stat(line : str, keyword : str) -> int:
	return int(re.sub(keyword + r'\s*:\s*([0-9]+).*', r'\1', line))


def extract_stats(clingologfilename : str) -> str:
	seconds = 0.0
	solve_seconds = 0.0

	keywords = ['Variables', 'Rules', 'Constraints', 'Choices', 'Conflicts']
	stats = dict()
	

	for line in open(clingologfilename,'r').readlines():
		for keyword in keywords:
			if line.startswith(keyword + ' '):
				stats[keyword.lower()] = extract_stat(line, keyword)
				continue
		if line.startswith(fnTime):
			match = re.sub(timeRegex, r'\1 \2', line)
			(seconds, solve_seconds) = tuple(map(lambda x: float(x), match.split(' ')))
	statstring = " ".join(list(map(lambda t: f"{t[0]}={t[1]}", stats.items())))


	return f'{statstring} seconds={seconds} solve_seconds={solve_seconds}'
