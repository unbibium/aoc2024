#!/usr/bin/python3

import os, sys
from collections import namedtuple

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

height_map = {}

for y, line in enumerate(sys.stdin.readlines()):
    for x,ch in enumerate(line.rstrip()):
        if '0' <= ch <= '9':
            height_map[ complex(x,y) ] = int(ch)

def find_summits(startpos, startheight=0):
    if startheight == 9: yield startpos
    next_steps = (startpos + pow(1j,d) for d in range(4))
    for pos in next_steps:
        if height_map.get(pos) == startheight+1:
            yield from find_summits(pos, startheight+1)

puzzle_2_score = puzzle_1_score = 0

for pos, h in height_map.items():
    if h == 0:
        all_paths = list(find_summits(pos))
        summits = set(all_paths)
        puzzle_1_score += len(summits)
        puzzle_2_score += len(all_paths)

print("puzzle 1:", puzzle_1_score)
print("puzzle 2:", puzzle_2_score)

