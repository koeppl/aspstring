#!/usr/bin/env zsh
## works with the files of https://github.com/jeanpttorres/dssp by stripping away the header

find -L datasets -name "*.dssp" -exec python3 gen/dssp2txt.py {} \;
find -L datasets -name "*.txt" -exec python3 gen/genlp.sh {} \;
