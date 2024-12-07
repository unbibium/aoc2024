#!/usr/bin/python3

import os, sys
from collections import namedtuple

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

crates = set()

guardgfx = { 1: '>', -1: '<', 0+1j:'v', 0-1j:'^' }

# puzzle 1
class Playfield:
    #def __init__(self, crates, guard, gdir=complex(0,-1)):
    def __init__(self, txtlines):
        self.crates = set()
        for y, line in enumerate(txtlines):
            for x, ch in enumerate(line.rstrip()):
                if ch == '#':
                    self.crates.add( complex(x,y) )
                elif ch == '^':
                    self.gpos = complex(x,y)
                    self.gdir = complex(0,-1)
        if x < 2:
            raise Exception("blank line at end")
        self.bound = complex(x+1,y+1)

        self.steps = set()
        self.turnpos = []
        self.turndir = []
        self.newobs = set()

    def one_step(self):
        while self.gpos + self.gdir in self.crates:
            # obstruction found, turn right
            self.gdir *= complex(0,1)
            # record turn for puzzle 2
            self.turnpos.append( self.gpos )
            self.turndir.append( self.gdir )
            # predict
            self.render()
            if len(self.turndir) >= 3:
                # see if last three turns can be completed
                # into a square loop
                # (this is inadqeuate -- need to consider all past turns can be repeated)
                print("last three turns:")
                for tpos, tdir in zip(self.turnpos[-3:], self.turndir[-3:]):
                    print(tpos, "   ", guardgfx[tdir])
                opposite=self.turnpos[-3]-self.turnpos[-2]
                print("Vector of 2nd line:", opposite, int(abs(opposite)))
                projected=int(abs(opposite))+1
                print("Projecting ahead", projected," steps to")
                if self.guard_can_move_forward(projected):
                    obstacle=( self.gpos + projected*self.gdir)
                    self.newobs.add(obstacle)
                    print("new obstacle at", obstacle)
                print()


        self.steps.add(self.gpos)
        self.gpos += self.gdir


    def guard_in_bounds(self):
        return 0 <= self.gpos.real < self.bound.real and \
                0 <= self.gpos.imag < self.bound.imag

    def guard_can_move_forward(self, moves):
        """
        Return true if the guard can step forward this many times
        unobstructed
        """
        for m in range(1,moves):
            if self.gpos + self.gdir * m in (self.crates | self.newobs):
                print("collision at ",m)
                return False
        return True

    def render(self):
        for y in range(int(self.bound.imag)):
            for x in range(int(self.bound.real)):
                pos = complex(x,y)
                if self.gpos == pos:
                    print(guardgfx.get(self.gdir,'G'), end='')
                elif pos in self.crates:
                    print('#',end='')
                elif pos in self.newobs:
                    print("O",end='')
                elif pos in self.turnpos:
                    print('+',end='')
                elif pos in self.steps:
                    print('x',end='')
                else:
                    print('.',end='')
            print('')
        print('')

pf = Playfield(sys.stdin.readlines())
pf.render()
print()
stepCount = 0
while(pf.guard_in_bounds()):
    stepCount += 1
    pf.one_step()
print("puzzle 1:", len(pf.steps))
print("puzzle 1:", len(pf.newobs))

