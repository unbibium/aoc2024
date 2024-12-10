#!/usr/bin/python3

import os, sys
import itertools

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

antennas = {}

for y, line in enumerate(sys.stdin.readlines()):
    for x, ch in enumerate(line.rstrip()):
        if '0' <= ch <= '9' or 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            antennas.setdefault(ch, set()).add( complex(x,y) )

maxx, maxy = x, y

def antinodes( positions ):
    result = set()
    for a, b in itertools.combinations(positions, 2):
        c = a + (b-a) * 2
        if 0 <= c.real <= maxx and 0 <= c.imag <= maxy:
            result.add(c)
        c = b + (a-b) * 2
        if 0 <= c.real <= maxx and 0 <= c.imag <= maxy:
            result.add(c)
    return result
    
map_anodes=set()
for frequency, positions in antennas.items():
    map_anodes.update( antinodes(positions) )

print("puzzle1: ", len(map_anodes))

def antinodes2( positions ):
    result = set()
    for a, b in itertools.combinations(positions, 2):
        c = a + (b-a)
        while 0 <= c.real <= maxx and 0 <= c.imag <= maxy:
            result.add(c)
            c += (b-a)
        c = b + (a-b)
        while 0 <= c.real <= maxx and 0 <= c.imag <= maxy:
            result.add(c)
            c += (a-b)
    return result

map_anodes=set()
for frequency, positions in antennas.items():
    map_anodes.update( antinodes2(positions) )

print("puzzle2:", len(map_anodes))

