# 🗂️  Encoding Hard String Problems with Answer Set Programming

Using answer set programming (ASP), we solve the problems 

 - Closest String (CSP)
 - Closest Substring (CSS)
 - Longest Common Subsequence (LCS)
 - Minimum Common String Partition (MCSP)
 - Shortest Common Superstring (SCS)

on small instances.

Required Software:

 - executable [clingo](https://github.com/potassco/clingo)
 - python3 package [tqdm](https://github.com/tqdm/tqdm) (eg. install via `pip3 install tqdm`)

Input Format: 

- All encodings expect an input in text form, where each line is interpreted as an input string.
- All strings are expected to have the same length.
- For the minimum common string partition problem, we read only the first two lines.

Runnable executables can be invoked by 
 - `bin/shortest_superstring.py --input <FILE>`
 computes the longest common superstring of `<FILE>`
 - `bin/closest_string.py --input <FILE>`
 computes the closest string of <FILE>
 - `bin/closest_string.py --input <FILE> --length <LEN>`
 computes the closest substring of `<FILE>` with length `<LEN>`
 - `bin/aspsolver.py --prg <PRG> --input <FILE>`
 computes PRG being either longest_common_subsequence or minimum_common_string_partition

For each solution, we addiionally have a brute-force implementation in the `brute` folder.
The parameters are identical except that we have for each problem an individual executable such that the parameter `--prg` does not exist.
 
Each script in the `bin` folder executes a couple of commands:
- first, it translates the plain file into a clingo readable file format, which is done by one of the scripts in the `translate` folder.
- second, it calls clingo with the specific ASP encoding found in the `encoding` folder
- finally, it calls the specific decoder to extract from the clingo log file the solution. The decoders can be found in the folder `decoder`

A manual step-by-step execution can be done as follows:
 - `translate/text2lp.py --input <TEXT-FILE> > <LP-FILE>`
 - `clingo encoding/closest_string.lp <LP-FILE> > <CLINGO-LOG>`
 - `decode/closest_string.py --input <TEXT-FILE> --log <CLINGO-LOG>`

# Datasets

The used datasets can be generated or downloaded with scripts in the `gen` folder.

 `gen/generate_datasets.sh` downloads and generates the datasets used in the paper. 
 It creates the directories
  - `covid19` with shuffled prefixes of the covid19 FASTA reference file
	- `random` for the randomly generated datasets
	- `dssp` from the [https://github.com/jeanpttorres/dssp](Distinguishing String Selection Problem) project


# Misc

To see whether the code runs correctly, you can execute the python scripts in the `test` folder.

The output can be further processed by [sqlplot](https://github.com/koeppl/sqlplot).
