#!/usr/bin/env python3

import time
from tqdm import tqdm
import argparse
from pathlib import Path 

# copied from LeetCode: Find the Shortest Superstring
# https://leetcode.com/problems/find-the-shortest-superstring/solutions/194891/official-solution/
def shortestSuperstring(strings, quiet = False):
		m = len(strings)

		# Populate overlaps
		overlaps = [[0] * m for _ in range(m)]
		for i, x in enumerate(strings):
				for j, y in enumerate(strings):
						if i != j:
								for ans in range(min(len(x), len(y)), -1, -1):
										if x.endswith(y[:ans]):
												overlaps[i][j] = ans
												break

		# dp[mask][i] = most overlap with mask, ending with ith element
		dp = [[0] * m for _ in range(1<<m)]
		parent = [[None] * m for _ in range(1<<m)]
		for mask in tqdm(range(1, 1 << m), disable=quiet):
				for bit in range(m):
						if (mask >> bit) & 1:
								# Let's try to find dp[mask][bit].  Previously, we had
								# a collection of items represented by pmask.
								pmask = mask ^ (1 << bit)
								if pmask == 0: continue
								for i in range(m):
										if (pmask >> i) & 1:
												# For each bit i in pmask, calculate the value
												# if we ended with word i, then added word 'bit'.
												value = dp[pmask][i] + overlaps[i][bit]
												if value > dp[mask][bit]:
														dp[mask][bit] = value
														parent[mask][bit] = i

		# Answer will have length sum(len(strings[i]) for i) - max(dp[-1])
		# Reconstruct answer:

		# Follow parents down backwards path that retains maximum overlap
		perm = []
		mask = (1<<m) - 1
		i = max(range(m), key = dp[-1].__getitem__)
		while i is not None:
				perm.append(i)
				mask, i = mask ^ (1<<i), parent[mask][i]

		# Reverse path to get forwards direction; add all remaining words
		perm = perm[::-1]
		seen = [False] * m
		for x in perm:
				seen[x] = True
		perm.extend([i for i in range(m) if not seen[i]])

		# Reconstruct answer given perm = word indices in left to right order
		ans = [strings[perm[0]]]
		for i in range(1, len(perm)):
				overlap = overlaps[perm[i-1]][perm[i]]
				ans.append(strings[perm[i]][overlap:])

		return "".join(ans)


parser = argparse.ArgumentParser(description='compute closest substring')
parser.add_argument("--input", type=str, help="input file")
parser.add_argument("--quiet", action=argparse.BooleanOptionalAction, help="no progress bar", default=False)
args = parser.parse_args()


plaininputfilename = Path(args.input)
inputbasename = Path(plaininputfilename).with_suffix('').name

strings=[]

with open(plaininputfilename, "r") as istream:
	strings = istream.read().splitlines() 

start_time = time.time()
superstring = shortestSuperstring(strings, args.quiet)

m = len(strings)
num_combinations = (1 << m) * m

print(f'RESULT type=scs method=brute input={inputbasename} length={len(superstring)} output={superstring} combinations={num_combinations} seconds={time.time() - start_time}')
