import re

def unary_function(fnname : str, coding :str):
	return int(re.sub(fnname + r'\(([0-9]+)\)', r'\1', coding))
def binary_function(fnname : str, coding :str):
	return tuple(map(lambda x: int(x), re.sub(fnname + r'\(([0-9]+),([0-9]+)\)', r'\1 \2', coding).split(' ')))

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

