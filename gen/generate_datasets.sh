#!/usr/bin/env bash
scriptpath=`dirname $(readlink -f "$0")`


## works with the files of https://github.com/jeanpttorres/dssp by stripping away the header
[[ -d dssp ]] || git clone https://github.com/jeanpttorres/dssp
find dssp -name "*.dssp" -exec $scriptpath/dssp2txt.py {} \;

mkdir -p covid19
[[ -f covid19/covid19-refseq.fasta ]] || wget 'https://raw.githubusercontent.com/cfarkas/SARS-CoV-2-freebayes/master/covid19-refseq.fasta' -O covid19/covid19-refseq.fasta
[[ -f covid19/covid19-refseq.txt ]] || tail -n '+2' covid19/covid19-refseq.fasta > covid19/covid19-refseq.txt
for n in $(seq 10 10 70); do
	# [[ -f covid19.${n}.txt ]] || 
	$scriptpath/shuffle_file.py --seed 1 --input covid19/covid19-refseq.txt --output covid19/covid19.${n}.txt --prefix ${n}
done

$scriptpath/random_datasets.py --folder "random"
