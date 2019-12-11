import sys
import copy
import itertools
import collections
from enum import IntEnum

class OP(IntEnum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    INCREMENT_RB = 9
    HALT = 99

# https://github.com/e-nomem/AdventOfCode/blob/master/2019/intcode/io.py

class VM:
    def __init__(self, program, phase = None):
        self.mem = collections.defaultdict(int)
        for i,d in enumerate(program):
            self.mem[i] = d
        self.RB = 0
        self.IP = 0
        if phase:
            self.set_param(1, phase)
            self.IP += 2

    def run(self, input = None):
        while self.mem[self.IP] != OP.HALT:
            # print(f"[{self.IP}] {self.mem[self.IP]}: {self.mem[self.IP+1]} {self.mem[self.IP+2]} {self.mem[self.IP+3]}")

            cmd = self.mem[self.IP] % 100

            if cmd == OP.ADD:
                self.set_param(3, self.param(1) + self.param(2))
                self.IP += 4
            elif cmd == OP.MULT:
                self.set_param(3, self.param(1) * self.param(2))
                self.IP += 4
            elif cmd == OP.INPUT:
                print(f"using input: {input}")
                self.set_param(1, input)
                self.IP += 2
            elif cmd == OP.OUTPUT:
                output = self.param(1)
                print(f"output: {int(output)}\n")
                self.IP += 2
                return int(output)
            elif cmd == OP.JUMP_IF_TRUE:
                self.IP = self.param(2) if self.param(1) else self.IP+3
            elif cmd == OP.JUMP_IF_FALSE:
                self.IP = self.param(2) if not self.param(1) else self.IP+3
            elif cmd == OP.LESS_THAN:
                self.set_param(3, self.param(1) < self.param(2))
                self.IP += 4
            elif cmd == OP.EQUAL:
                self.set_param(3, self.param(1) == self.param(2))
                self.IP += 4
            elif cmd == OP.INCREMENT_RB:
                self.RB += self.param(1)
                # print(f"RB: {self.RB}")
                self.IP += 2
            else: # op_err
                print(f"Unknown opcode: {self.mem[self.IP]} ")
                sys.exit(-1)

        # print("[END]\n")
        return None

    @property
    def is_running(self):
        return self.mem[self.IP] != 99

    def mode(self, n):
        return (self.mem[self.IP] // (10**(n+1))) %10

    def param(self, n):
        if self.mode(n) == 2:
            return self.mem[self.RB+self.mem[self.IP+n]]
        elif self.mode(n) == 1:
            return self.mem[self.IP+n]
        else:
            return self.mem[self.mem[self.IP+n]]

    def set_param(self, n, val):
        if self.mode(n) == 2:
            self.mem[self.RB+self.mem[self.IP+n]] = val
        elif self.mode(n) == 1:
            self.mem[self.IP+n] = val
        else:
            self.mem[self.mem[self.IP+n]] = val

with open("input.txt","r") as f:
    instructions = [int(i.strip()) for i in f.read().split(',')]



# class fakeVM:
#     insts = [1,0, 0,0, 1,0, 1,0, 0,1, 1,0, 1,0]
#     cur_inst = 0
#
#     def run(self, input = None):
#         if self.cur_inst >= len(self.insts):
#             return None
#         ret = self.insts[self.cur_inst]
#         self.cur_inst += 1
#         print(f"output: {ret}\n")
#         return ret
#
#     @property
#     def is_running(self):
#         return self.cur_inst < len(self.insts)
#


import numpy as np
hull = np.zeros((45,10), 'int')
pos = [1,1]
dir = 0
dirs = ((0,-1),(1,0),(0,1),(-1,0))

# robot = fakeVM()

robot = VM(instructions)

# Part 1
painted = np.zeros(hull.shape, 'int')

# Part 2:
hull[pos[0]][pos[1]] = 1

while robot.is_running:
    print(f"colour at current pos: {hull[pos[0]][pos[1]]}")
    paint_color = robot.run(hull[pos[0]][pos[1]])
    if paint_color is None:
        break
    hull[pos[0]][pos[1]] = paint_color
    painted[pos[0]][pos[1]] = 1
    print(f"Painted {pos[0]},{pos[1]}: {hull[pos[0]][pos[1]]}")

    dir = (dir + [-1,1][robot.run()]) % 4
    print(f"New dir: {dirs[dir]}")
    pos[0] += dirs[dir][0]
    pos[1] += dirs[dir][1]
    print(f"New pos: {pos}")

print(f"Total white: {np.count_nonzero(hull)}, Total painted once: {np.count_nonzero(painted)}")

print("\n".join(''.join([u"⬛️",u"⬜️"][int(i)] for i in line) for line in hull.transpose()))
