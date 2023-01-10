import re
from pathlib import Path
import typing as t

def split_keyvalueline(line: str) -> t.Mapping[str,str]:
	""" read a line of 'key=value' pairs separated by whitespace(s) into a dict """
	attrs=dict()
	while line.find('=') != -1:
		key = line[:line.find('=')]
		valuematch = re.match(r'^\S+', line[line.find('=')+1:])
		assert valuematch, 'invalid key/value line: %s' % line
		value = valuematch.group(0)
		line=line[len(key)+len(value)+1:]
		key = key.strip()
		value = value.strip()
		attrs[key] = value
	return attrs

def split_resultline(line: str) -> t.Mapping[str,str]:
	""" read a RESULT line and put the keyvalue pairs into a dict """
	return split_keyvalueline(line[len('RESULT '):].strip())

def extract_result(filename : Path):
	for line in open(filename,'r').readlines():
		if line.startswith('RESULT '):
			return split_resultline(line)
