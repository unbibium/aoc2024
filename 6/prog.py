#!/usr/bin/python3

import os, sys
from collections import namedtuple

if sys.stdin.isatty():
    print("redirect input")
    sys.exit(2)

crates = set()

guardgfx = { 1: '>', -1: '<', 0+1j:'v', 0-1j:'^' }

class XY(complex):
    def __str__(self):
        return "<%d,%d>" % (self.real, self.imag)
    def repr(self):
        return str(self)
    def __add__(self, other):
        if isinstance(other,int):
            return XY(super().__add__(complex(other,1)))
        return XY(super().__add__(other))
    def __mul__(self, other):
        return XY(super().__mul__(other))

# a quirk of complex numbers is that multiplying by "i"
# is the same as turning right 90 degrees
turn_right = XY(0,1)

# puzzle 1
class Playfield:
    def __init__(self, txtlines):
        self.crates = set()
        for y, line in enumerate(txtlines):
            for x, ch in enumerate(line.rstrip()):
                if ch == '#':
                    self.crates.add( XY(x,y) )
                elif ch == '^':
                    self.gpos = XY(x,y)
                    self.gdir = XY(0,-1)
        if x < 2:
            raise Exception("blank line at end")
        self.bound = XY(x+1,y+1)

        self.steps = set()
        self.turnpos = []
        self.turndir = []
        self.turns = set()
        self.newobs = set()

    def one_step(self):
        while self.gpos + self.gdir in self.crates:
            # obstruction found, turn right
            self.gdir *= turn_right
            # record turn for puzzle 2
            #self.turnpos.append( self.gpos )
            #self.turndir.append( self.gdir )
            # record entire vector so we can search for both
            self.turns.add( (self.gpos, self.gdir) )

        self.imagine_obstacle()

        # move guard
        self.steps.add(self.gpos)
        self.gpos += self.gdir

    def place_new_obstacle(self):
        # one step in front of us
        self.newobs.add(self.gpos+self.gdir)

    def imagine_obstacle(self):
        # first, look to our right
        rdir = self.gdir * turn_right
        rpos = self.gpos
        # if we walk there starting from here,
        # and find an old turn, then placing an
        # obstacle in front of us will be correct
        sight = set()
        while self.in_bounds(rpos):
            # turn to avoid crates
            while rpos+rdir in self.crates:
                rdir *= turn_right
                # is this a turn the guard actually made?
                if (rpos, rdir) in self.turns:
                    print("walked into a previous turn", rpos, rdir, "after", len(sight), "steps")
                    self.place_new_obstacle()
                    return
            # is it a new loop?
            sight.add( (rpos, rdir) )
            rpos += rdir
            if (rpos, rdir) in sight:
                print("somehow walked in a circle for ", len(sight), "steps from", self.gpos)
                print("  circle starts at", rpos, rdir)
                self.place_new_obstacle()
                return

    def in_bounds(self, pos):
        return 0 <= pos.real < self.bound.real and \
                0 <= pos.imag < self.bound.imag

    def guard_in_bounds(self):
        return self.in_bounds(self.gpos)

    def render(self):
        for y in range(int(self.bound.imag)):
            for x in range(int(self.bound.real)):
                pos = XY(x,y)
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
while(pf.guard_in_bounds()):
    pf.one_step()

pf.render()

print("crates:", len(pf.crates))
print("puzzle 1:", len(pf.steps))
print("puzzle 2:", len(pf.newobs))
print("puzzle 2:", len(pf.newobs-pf.crates))

if len(pf.newobs) <= 1104:
    print("too low")
if len(pf.newobs) >= 3453:
    print("too low")
if len(pf.newobs) == 1657:
    print("incorrect")
if len(pf.newobs) == 1642:
    print("incorrect (try 5)")


