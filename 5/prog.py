#!/usr/bin/python3

import os, sys
from collections import namedtuple

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

rules = []
updates = []

Rule = namedtuple("Rule", "before after")

for line in sys.stdin.readlines():
    if '|' in line:
        rules.append(Rule(*map(int,line.rstrip().split('|'))))
    elif ',' in line:
        updates.append( list(map(int, line.rstrip().split(','))))

# puzzle 1: sum of middle page of correct updates
result1=0
# puzzle 2: 
result2=0

def is_correct(u): 
    for r in rules:
        if r.before in u and r.after in u and u.index(r.after) < u.index(r.before):
            return False
    return True

def corrected(u, recurse=0):
    for i, page in enumerate(u):
        for r in rules:
            if r.before in u and r.after in u:
                bi, ai = u.index(r.before), u.index(r.after)
                if bi > ai:
                    u[bi], u[ai] = u[ai], u[bi]
    if not is_correct(u):
        if recurse<99:
            return corrected(u, recurse+1)
        print("recursion error for", u)
        raise Exception("recursion")
    return middle_page(u)

def middle_page(u):
    return u[ (len(u)-1)//2 ]

for u in updates:
    if is_correct(u):
        # add page number of middle page
        result1 += middle_page(u)
    else:
        result2 += corrected(u)

print("puzzle 1:", result1)
print("puzzle 2:", result2)



