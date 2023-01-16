#!/usr/bin/env zsh

. /usr/bin/env_parallel.zsh

set -x
set -e


# for dataset in sample.txt; do
# 	./bin/fileinfo.py --input "$dataset"
#
# 	./bin/closest_string.py --input "$dataset" 
# 	./bin/closest_string.py --input "$dataset" --length 5
#
# 	./brute/closest_string.py --quiet --input "$dataset"
# 	./brute/closest_string.py --quiet --input "$dataset" --length 5
#
# 	for prg in longest_common_subsequence shortest_superstring minimum_common_string_partition; do
# 		./brute/${prg}.py --quiet --input "$dataset"
# 	done
# 	for prg in longest_common_subsequence shortest_superstring_permutation minimum_common_string_partition; do
# 		./bin/aspsolver.py --input "$dataset" --prg "$prg" 
# 	done
# 	./bin/shortest_superstring.py --input "$dataset"
# done

function evaluate_csp {
	dataset="$1"
	./bin/fileinfo.py --input "$dataset"
	./bin/closest_string.py --input "$dataset" 
	./brute/closest_string.py --quiet --input "$dataset"
	for length in 7 8 9; do
		./brute/closest_string.py --quiet --input "$dataset" --length "$length"
		./bin/closest_string.py --input "$dataset" --length "$length"
	done
}

function evaluate_lcs {
	dataset="$1"
	./bin/fileinfo.py --input "$dataset"
	./bin/aspsolver.py --input "$dataset" --prg "longest_common_subsequence" 
	./brute/longest_common_subsequence.py --quiet --input "$dataset"
}

function evaluate_scs {
	dataset="$1"
	./bin/fileinfo.py --input "$dataset"
	./bin/shortest_superstring.py --input "$dataset" 
	./brute/shortest_superstring.py --quiet --input "$dataset"
}

function evaluate_mcsp {
	dataset="$1"
	./bin/fileinfo.py --input "$dataset"
	./bin/aspsolver.py --input "$dataset" --prg "minimum_common_string_partition" 
 	./brute/minimum_common_string_partition.py --quiet --input "$dataset"
}
echo evaluation/scs/*.txt | xargs -n1 | env_parallel evaluate_scs
echo evaluation/mcsp/*.txt | xargs -n1 | env_parallel evaluate_mcsp
echo evaluation/lcs/*.txt | xargs -n1 | env_parallel evaluate_lcs
echo evaluation/csp/*.txt | xargs -n1 | env_parallel evaluate_csp

# echo evaluation/mcsp/*.txt > mcsp_datasets.txt

# echo evaluation/2*.txt > datasets_mcsp.txt
#
# xargs -n1 < datasets.txt	| env_parallel evaluate 
# xargs -n1 < datasets_mcsp.txt | env_parallel evaluate_mcsp
