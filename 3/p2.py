#!/usr/bin/python3

import os, sys

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

reports = []

# todo: figure out how to sort while inputting
code = sys.stdin.read()

import re

inst_re = re.compile(r'''
                    (do|don't|mul)
                    \(
                    ([0-9,]*)
                    \)
                    ''', re.MULTILINE + re.VERBOSE)

result=0
enabled=True
for m in inst_re.finditer(code):
    f, op = m.groups()
    print(f, op)
    if f == "do" and op == '':
        enabled=True
    elif f == "don't" and op == '':
        enabled=False
    elif f == "mul" and enabled and op.count(',') == 1:
        g1,g2 = op.split(',')
        result += int(g1)*int(g2)

print(result)

