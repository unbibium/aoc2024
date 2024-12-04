#!/usr/bin/python3

import os, sys

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

left = []
right = []

# todo: figure out how to sort while inputting
for line in sys.stdin.readlines():
    words = line.rstrip().split()
    if len(words) != 2: continue
    left.append(int(words[0]))
    right.append(int(words[1]))

left.sort()
right.sort()

# puzzle 1
print(sum(abs(lnum-rnum) for lnum, rnum in zip(left, right)))
# puzzle 2
print(sum(lnum*right.count(lnum) for lnum in left))

