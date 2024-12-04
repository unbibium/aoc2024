#!/usr/bin/python3

import os, sys
from collections import defaultdict

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

lettermap = defaultdict(list)

for y, line in enumerate(sys.stdin.readlines()):
    for x, ch in enumerate(line):
        if ch in 'XMAS':
            lettermap[ch].append( complex(x,y) )

def each_direction():
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            if dx == dy == 0:
                continue
            yield list(complex(dx,dy)*i for i in range(5))

#          M   M   A    S   S
x_shape = (0, 2j, 1+1j, 2, 2+2j)

def each_x():
    for r in range(4):
        yield list( dxy * (1j ** r) for dxy in x_shape )

# search for word
def search(word, func=each_direction):
    l = list(func())
    results = 0
    for pos in lettermap[word[0]]:
        results += matches_from_pos(word, pos, l)
        pass
    return results

def matches_from_pos(word, pos, l):
    results = 0
    for dlist in l:
        for i, ch in enumerate(word[1:],1):
            if pos+dlist[i] not in lettermap[ch]: break
        else: # loop completed without break
            results += 1
    return results

print(search('XMAS'))

print(search('MMASS',each_x))

