#!/usr/bin/python3
#
# at no point do we need to know the arrangement of the stones, just
# how many stones have each number on them.  so we just use a
# histogram and apply the rules to that.

import os, sys,math 
import logging
from collections import defaultdict

def blink(pile):
    newpile = defaultdict(int)
    for key in pile:
        if key == 0:
            newpile[1] += pile[key]
        elif key == 1:
            newpile[2024] += pile[key]
        elif int(math.log10(key)) % 2 == 1: # even number of digits
            key1, key2 = divmod(key, pow(10,int(math.log10(key)+1)/2))
            newpile[int(key1)] += pile[key]
            newpile[int(key2)] += pile[key]
        else:
            newpile[key*2024] += pile[key]
    return newpile

# tests from page
assert blink( {125:1,17:1} ) == {253000:1, 1: 1, 7: 1}
assert blink( {253000:1, 1: 1, 7: 1} ) == { 253:1, 0:1, 2024:1, 14168:1 }
assert blink( { 253:1, 0:1, 2024:1, 14168:1 } ) == { 512072:1, 1:1, 20:1, 24:1, 28676032:1 }
assert blink({ 512072:1, 1:1, 20:1, 24:1, 28676032:1 } ) == { 512:1, 72:1, 2024:1, 2:2, 0:1, 4:1, 2867:1, 6032:1 }
# ok I don't feel like copying them all let's just do this

testData = {125:1,17:1}
for i in range(25):
    testData = blink(testData)

assert (sum(testData.values())) == 55312

# ok, got this far

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

stones = list(map(int,sys.stdin.read().rstrip().split()))

stoneCounts = defaultdict(int)
for stone in stones:
    stoneCounts[stone] += 1

print(stoneCounts)

for i in range(25):
    stoneCounts=blink(stoneCounts)

print("puzzle 1:", sum(stoneCounts.values()))
print("    keys:", len(stoneCounts))

for i in range(50): #more, lightning fast
    stoneCounts=blink(stoneCounts)

print("puzzle 2:", sum(stoneCounts.values()))
print("    keys:", len(stoneCounts))
