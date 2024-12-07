#!/usr/bin/python3

import os, sys
from collections import namedtuple

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

crates = set()

data = []

for line in sys.stdin.readlines():
    if ':' not in line: continue
    left, right = line.rstrip().split(': ')
    right = list(map(int, right.split()))
    data.append( (int(left), right) )

# fix names before writing the rest, please

