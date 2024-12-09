#!/usr/bin/python3

import os, sys
from collections import namedtuple

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

def get_disk(f):
    disk = []
    fileId = 0
    free = False
    for char in f.read():
        if char in "\n\r": break
        sectors = int(char)
        if free:
            disk += [None] * sectors 
        else:
            disk += [fileId] * sectors 
            fileId += 1
        free = not free
    return disk


fileId = 0

disk = get_disk(sys.stdin)

def is_complete(disk):
    return all(sector is None for sector in disk[-disk.count(None):])
assert is_complete( [2,2,2,None,None] )
assert not is_complete( [2,None,2,2,None] )

searchIndex=len(disk)
firstNoneSector = 0
while True:
    try:
        firstNoneSector = disk.index(None, firstNoneSector, searchIndex)
    except:
        break
    searchIndex -= 1
    if disk[searchIndex] is None:
        continue
    disk[firstNoneSector], disk[searchIndex] = disk[searchIndex], disk[firstNoneSector]

#print(disk)
print(sum(a*b for a,b in enumerate(disk) if b))


