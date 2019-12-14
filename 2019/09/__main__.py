import copy
import itertools
import collections
from enum import IntEnum
from ..utils import inputFile

class OP(IntEnum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    INCREMENT_RB = 9
    HALT = 99

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

    def run(self, input):
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
                print(f"output: {output}\n")
                self.IP += 2
                # return output
            elif cmd == OP.JUMP_IF_TRUE:
                self.IP = self.param(2) if self.param(1) else self.IP+3
            elif cmd == OP.JUMP_IF_FALSE:
                self.IP = self.param(2) if not self.param(1) else self.IP+3
            elif cmd == OP.LESS_THAN:
                self.set_param(3, self.param(1) < self.param(2))
                self.IP += 4
            elif cmd == OP.EQUALS:
                self.set_param(3, self.param(1) == self.param(2))
                self.IP += 4
            elif cmd == OP.INCREMENT_RB:
                self.RB += self.param(1)
                # print(f"RB: {self.RB}")
                self.IP += 2
            else: # op_err
                raise(Exception(f"*** Unknown opcode: {self.mem[self.IP]} ***"))

        # print("[END]\n")
        return 0

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


with open(inputFile()) as f:
    instructions = [int(i.strip()) for i in f.read().split(',')]

print("Part 1:")
VM(instructions).run(1)
# 2494485073

print("Part 2:")
VM(instructions).run(2)
# 44997
