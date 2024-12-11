#!/usr/bin/python3

import os, sys,math 

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
        5: (2024, 1, 2024, 2024),
        6: (20,24, 2024, 20,24, 20,24),
        7: (2,0,2,4, 20,24, 2,0,2,4, 2,0,2,4),
        8: (2024,1,2024,2024, 2,0,2,4, 2024,1,2024,2024, 2024,1,2024,2024)
        }

while len(lenzero) < 78:
    lenzero.append( lenzero[-3]*3 + lenzero[-4] )
    #print(len(zero)-1, len(zero[-1]), lenzero[-1])


def blinkone(stone, ct):
    """
    Blink a single stone the requisite number of times
    return the length of the resulting list
    """
    if hasattr(stone, '__len__'):
        return sum(map(lambda x: blinkone(x,ct), stone))
    if ct == 0:
        return 1
    if stone == 0:
        return lenzero[ct]
    elif stone == 1:
        return lenzero[ct-1]
    elif stone == 2024:
        return lenzero[ct-2]
    elif int(math.log10(stone)) % 2 == 1:
        stone1, stone2 = divmod(stone, pow(10,int(math.log10(stone)+1)/2))
        print("split", stone, "into",stone1,stone2,"for",ct-1,"more blinks")
        return blinkone(stone1, ct-1) + blinkone(stone2, ct-1)
    else:
        print("multiplying",stone,"into",stone*2024,"for",ct-1,"more blinks")
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

for i in range(1,26):
    print(i,blinkone(test2,i))

assert blinkone(test2,1) == 3
assert blinkone(test2,2) == 4
assert blinkone(test2,3) == 5
assert blinkone(test2,4) == 9
assert blinkone(test2,5) == 13
assert blinkone(test2,6) == 22
print( blinkone(test2,25) )
assert blinkone(test2,25) == 55312


# get 25 blinks
result1 = stones.copy()
for i in range(25):
    result1 = blink(result1)

print(len(list(result1)))
print( sum(map(lambda x: blinkone(x,25),stones)) )



