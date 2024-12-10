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

def puzzle1(indisk):
    disk=indisk.copy()
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
    return disk

def puzzle2(indisk):
    disk=indisk.copy()
    # start with highest id
    maxFileId = max(filter(None,disk))
    for fileId in range(maxFileId,0,-1):
        sourceLeft = disk.index(fileId)
        for sourceRight,sector in enumerate(disk[sourceLeft:],sourceLeft):
            if sector != fileId:
                break
        else: #no blank sectors at end
            sourceRight += 1 # compensate for edge case
        sourceLength = sourceRight-sourceLeft
        destRangeLeft = disk.index(None)
        if sourceLeft < destRangeLeft:
            break # no more room to the left of source
        for destLeft in range(destRangeLeft,sourceLeft):
            destRight = destLeft+sourceLength
            if all(sector is None for sector in disk[destLeft:destRight]):
                # perform swap
                disk[sourceLeft:sourceRight], disk[destLeft:destRight] = disk[destLeft:destRight], disk[sourceLeft:sourceRight]
                break # and continue outer loop
    return disk

disk1 = puzzle1(disk)
print(sum(a*b for a,b in enumerate(disk1) if b))
disk2 = puzzle2(disk)
print(sum(a*b for a,b in enumerate(disk2) if b))


