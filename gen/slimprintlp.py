#!/usr/bin/env python3

import sys
import re

for line in open(sys.argv[1], "r").read().splitlines():
    line = line.strip()
    if len(line) == 0:
        continue
    if line.startswith("%"):
        continue
    if line.find("%% (") == -1:
        print(line)
        continue
    print(re.sub(r'%% \(([^)]+)\)', r'%% (\\ref{eq\1})', line))
