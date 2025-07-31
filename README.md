# Encoding Hard String Problems with Answer Set Programming
![automatic test](https://github.com/koeppl/aspstring/actions/workflows/check.yml/badge.svg)

We solve the following problems with answer set programming (ASP)

 - Closest String (CSP)
 - Closest Substring (CSS)
 - Longest Common Subsequence (LCS)
 - Minimum Common String Partition (MCSP)
 - Shortest Common Superstring (SCS)

## Required Software

 - executable [clingo](https://github.com/potassco/clingo)
 - python3 package [tqdm](https://github.com/tqdm/tqdm) (eg. install via `pip3 install tqdm`)

## Input Format

- All encodings expect an input in text form, where each line is interpreted as an input string.
- All strings are expected to have the same length.
- For the minimum common string partition problem, we read only the first two lines.

## Usage

Runnable executables can be invoked by 
 - `bin/shortest_superstring.py --input <FILE>`
 computes the longest common superstring of `<FILE>`
 - `bin/closest_string.py --input <FILE>`
 computes the closest string of <FILE>
 - `bin/closest_string.py --input <FILE> --length <LEN>`
 computes the closest substring of `<FILE>` with length `<LEN>`
 - `bin/aspsolver.py --prg <PRG> --input <FILE>`
 computes PRG being either `longest_common_subsequence` or `minimum_common_string_partition`

If there are multiple alternative encodings to choose, there should be an option `--flavor `
Current flavors are:
 - none: Without this argument, the default (currently best) implementation will be run.
 This is currently due to an anonymous reviewer of CPM 2023
 - `--flavor cpm`: use the encoding as described in the conference paper at CPM 2023

## Structure

For each solution, we additionally have a brute-force implementation in the `brute` folder.
The parameters are identical except that we have for each problem an individual executable such that the parameter `--prg` does not exist.
 
Each script in the `bin` folder executes a couple of commands:
- first, it translates the plain file into a clingo readable file format, which is done by one of the scripts in the `translate` folder.
- second, it calls clingo with the specific ASP encoding found in the `encoding` folder
- finally, it calls the specific decoder to extract the solution from the clingo log file. The decoders can be found in the folder `decoder`

A manual step-by-step execution can be done as follows for computing the closest string:
 - `translate/text2lp.py --input <TEXT-FILE> > <LP-FILE>`
 - `clingo encoding/closest_string/closest_string.lp <LP-FILE> > <CLINGO-LOG>`
 - `decode/closest_string.py --input <TEXT-FILE> --log <CLINGO-LOG>`

# Datasets and Examples

The used datasets can be generated or downloaded with the scripts in the `gen` folder.

 `gen/generate_datasets.sh` downloads and generates the datasets used in the paper. 
 It creates the directories
  - `covid19` with shuffled prefixes of the covid19 FASTA reference file
  - `random` for the randomly generated datasets
  - `dssp` from the [Distinguishing String Selection Problem](https://github.com/jeanpttorres/dssp) project

## Sample Run

```shell
mkdir dataset
cd dataset
../gen/generate_datasets.sh
../bin/closest_string.py --input dssp/instances/g3/rand-4-50-50-10-1.txt
../bin/closest_string.py --length 3 --input random/csp/s05m07n009i1.txt
../bin/aspsolver.py --prg minimum_common_string_partition --input covid19/covid19.10.txt
../bin/aspsolver.py --prg longest_common_subsequence --input random/lcs/s02m05n022i1.txt
../bin/shortest_superstring.py --input random/scs/s02m10n008i0.txt
```

## Examples in the Paper

The solutions to the figures in the paper can be revalidated with the files in the `sample` folder with the name 
`sleeplessness.{PRG}.txt`:

with ASP:

```shell
./bin/closest_string.py --input sample/sleeplessness.csp.txt
./bin/closest_string.py --length 4 --input sample/sleeplessness.css.txt
./bin/aspsolver.py --prg longest_common_subsequence --input sample/sleeplessness.lcs.txt
./bin/aspsolver.py --prg minimum_common_string_partition --input sample/sleeplessness.mcsp.txt
./bin/shortest_superstring.py --input sample/sleeplessness.scs.txt
```

with python implementations of the brute-force algorithms:

```shell
./brute/closest_string.py --input sample/sleeplessness.csp.txt
./brute/closest_string.py --length 4 --input sample/sleeplessness.css.txt
./brute/longest_common_subsequence.py --input sample/sleeplessness.lcs.txt
./brute/shortest_superstring.py --input sample/sleeplessness.scs.txt
./brute/minimum_common_string_partition.py --input sample/sleeplessness.mcsp.txt 
```
Note that the last call will take a long time to finish.

# Misc

To check whether the code runs correctly, you can execute the python scripts in the `test` folder.


The output can be further processed by [sqlplot](https://github.com/koeppl/sqlplot).

# Reference

The results are published at CPM'24, and can be referenced as:

Dominik Köppl. Encoding Hard String Problems with Answer Set Programming. In 34th Annual Symposium on Combinatorial Pattern Matching (CPM 2023). Leibniz International Proceedings in Informatics (LIPIcs), Volume 259, pp. 17:1-17:21, Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2023).
[https://doi.org/10.4230/LIPIcs.CPM.2023.17](https://doi.org/10.4230/LIPIcs.CPM.2023.17)
