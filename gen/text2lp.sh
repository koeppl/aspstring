#!/usr/bin/env zsh
## wrapper around text2lp.py

python3 gen/text2lp.py "$1" > $1:r.lp
