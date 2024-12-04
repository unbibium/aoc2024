#!/usr/bin/python3

import os, sys

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

reports = []

# todo: figure out how to sort while inputting
code = sys.stdin.read()

import re

mul_re = re.compile(r'''
                    mul\(
                    (\d+),(\d+)
                    \)
                    ''', re.MULTILINE + re.VERBOSE)

result=0
for m in mul_re.finditer(code):
    g1, g2 = m.groups()
    result += int(g1)*int(g2)

print(result)

