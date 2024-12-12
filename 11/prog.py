#!/usr/bin/python3
#
# this probably counts as "brute force"
# I tried to optimize that, then I remembered I could just
# replace the list with a histogram.

import os, sys,math 
import logging

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

stones = list(map(int,sys.stdin.read().rstrip().split()))

zero = [(0, ),
       (1, ),
        (2024, ),
        (20, 24, ),
        (2,0, 2,4, )
        ]
lenzero = [ 1,1,1,2,4 ]

calczero = {
        5: (4048, 1, 4048, 8096),
        6: (40,48, 2024, 40,48, 80,96),
        7: (4,0,4,8, 20,24, 4,0,4,8, 8,0,9,6),
        8: (8096,1,8096,16192, 2,0,2,4, 8096,1,8096,16192, 8096,1,8096,16192)
        }

while len(lenzero) < 78:
    lenzero.append( lenzero[-3]*3 + lenzero[-4] )
    zero.append( lenzero[-3]*3 + lenzero[-4] )

    #print(len(zero)-1, len(zero[-1]), lenzero[-1])


def blinkone(stone, ct):
    """
    Blink a single stone the requisite number of times
    return the length of the resulting list
    """
    print(ct,end='')
    if hasattr(stone, '__len__'):
        return sum(map(lambda x: blinkone(x,ct), stone))
    if ct == 0:
        #print("counting",stone)
        print("A",end='')
        return 1
    if stone == 0:
        #print("0 with", ct,"blinks left, counting ", lenzero[ct-0], "stones")
        print("B",end='')
        return lenzero[ct+0]
    elif stone == 1:
        #print("1 with", ct,"blinks left, counting ", lenzero[ct+1], "stones")
        print("C",end='')
        return lenzero[ct+1]
    elif int(math.log10(stone)) % 2 == 1:
        stone1, stone2 = divmod(stone, pow(10,int(math.log10(stone)+1)/2))
        #print("split", stone, "into",stone1,stone2,"for",ct-1,"more blinks")
        print("E",end='')
        return blinkone(int(stone1), ct-1) + blinkone(int(stone2), ct-1)
    else:
        #print("multiplying",stone,"into",stone*2024,"for",ct-1,"more blinks")
        print("F",end='')
        return blinkone(stone*2024,ct-1)

# old brute force solution
def blink(stones):
    for stone in stones:
        if stone == 0:
            yield 1
        elif int(math.log10(stone)) % 2 == 1:
            yield from divmod(stone, pow(10,int(math.log10(stone)+1)/2))
        else:
            yield stone*2024

print("---")
test1 = [0, 1, 10, 99, 999]

assert list(blink(test1)) == [ 1, 2024, 1,0,9,9,2021976 ]

test2 = [125,17]

result2a = list(blink(test2))
assert result2a == [253000,1,7]
result2b = list(blink(result2a))
assert result2b == [253,0,2024,14168]
result2c = list(blink(result2b))
assert result2c == [512072,1,20,24,28676032]
result2d = list(blink(result2c))
assert result2d == [512,72,2024,2,0,2,4,2867,6032]

print(blinkone(test2,6))

# these extra asserts will save the whole thing
# left side
assert blinkone(125,2) == 2   # 253 0
assert blinkone(125,3) == 2   # 512872 1
assert blinkone(125,4) == 3   # 512 72 2024
assert blinkone(125,5) == 5   # 1036288 7 2 20 24
assert blinkone(125,6) == 7 # 2... 14168 4048 2 0 2 4
# right side
assert blinkone(17,2) == 2   # 2024 14168
assert blinkone(17,3) == 3   # 20 24 29676032
assert blinkone(17,4) == 6   # 2 0 2 4 2867 6032
assert blinkone(17,5) == 8   # 4048 1 4048...
assert blinkone(17,6) == 15  # 40 48 2024 40 48 88 96 and 8 more

def diagnose(oldStones, newStones):
    raise KeyError("aaab")

assert blinkone(test2,5) == 13
assert blinkone(test2,6) == 22
resultTest = stones.copy()
for i in range(1,25):
    oldResultTest = resultTest.copy()
    resultTest=list(blink(resultTest))
    left = blinkone(125,i)
    right = blinkone(17,i)
    print(i, left, "+", right, "=", left+right, "  ==  ", len(resultTest), file=sys.stderr)
    if left+right != len(resultTest):
        if len(resultTest) == blinkone(oldResultTest,1):
            print("error was before step", i)
            raise OverflowError("aaa")
        diagnose(oldResultTest,resultTest)


assert test25 == 55312
# get 25 blinks
result1 = stones.copy()
for i in range(25):
    result1 = blink(result1)

print(len(list(result1)))
print( sum(map(lambda x: blinkone(x,25),stones)) )



