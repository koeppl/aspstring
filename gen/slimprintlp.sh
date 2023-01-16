#!/usr/bin/env zsh
scriptpath=`dirname $(readlink -f "$0")`


mkdir -p slimprintlp
for i in closest_string closest_substring longest_common_subsequence shortest_superstring minimum_common_string_partition; do
	python3 $scriptpath/splimprint.py $scriptpath/../encoding/$i.lp > slimprintlp/$i.lp
done
