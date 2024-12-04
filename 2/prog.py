#!/usr/bin/python3

import os, sys

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

reports = []

# todo: figure out how to sort while inputting
for line in sys.stdin.readlines():
    report = line.rstrip().split()
    if len(report) == 0: continue
    reports.append(list(map(int,report)))

def isSafe(aReport):
    prev=descFlag=None
    for i, level in enumerate(aReport):
        if prev is not None:
            if abs(prev-level) not in (1,2,3): return False
            if descFlag is None:
                descFlag=prev>level
            elif (prev>level) != descFlag:
                return False
        prev=level
    return True

def isSafe2(aReport):
    for i in range(len(aReport)):
        subReport=aReport[:i] + aReport[i+1:]
        if isSafe(subReport):
            return True
    return False



# puzzle 1
print("puzzle 1:", sum(map(isSafe,reports)))
print("puzzle 1:", sum(map(isSafe2,reports)))

