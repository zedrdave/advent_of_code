import itertools
import asyncio

from ..intcode.VM import VM as VMBase
from ..utils import loadCSVInput, dprint, setVerbosity

# Debug:
setVerbosity(True)

# 1047153

#### COPY from VM
import sys
import copy
import itertools
import collections
from enum import IntEnum
from ..utils import dprint

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

# Heavily inspired from:
# https://github.com/e-nomem/AdventOfCode/blob/master/2019/intcode/io.py

async def stdin():
    while True:
        yield int(input('(input)> '))

async def stdout(val: int):
    print(f'(output)> {val}')

class VM(VMBase):
    def __init__(self, program, input = stdin, output = stdout, phase = None):
        self.mem = collections.defaultdict(int)
        for i,d in enumerate(program):
            self.mem[i] = d
        self.RB = 0
        self.IP = 0
        self.input = input
        self.output = output
        if phase:
            self.set_param(1, phase)
            self.IP += 2

    async def run(self):
        while self.mem[self.IP] != OP.HALT:
            dprint(f"[{self.IP}] {self.mem[self.IP]}: {self.mem[self.IP+1]} {self.mem[self.IP+2]} {self.mem[self.IP+3]}")

            cmd = self.mem[self.IP] % 100

            if cmd == OP.ADD:
                self.set_param(3, self.param(1) + self.param(2))
                self.IP += 4
            elif cmd == OP.MULT:
                self.set_param(3, self.param(1) * self.param(2))
                self.IP += 4
            elif cmd == OP.INPUT:
                input = self.input()
                if input is None:
                    raise(Exception("Missing input!"))
                dprint(f"using input: {input}")
                self.set_param(1, int(input))
                self.IP += 2
            elif cmd == OP.OUTPUT:
                output = int(self.param(1))
                dprint(f"output: {output}\n")
                self.IP += 2
                self.output(output)
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
                # dprint(f"RB: {self.RB}")
                self.IP += 2
            else: # op_err
                dprint(f"Unknown opcode: {self.mem[self.IP]} ")
                sys.exit(-1)

        dprint("[HALT]\n")
        # return None


instructions = [int(i) for i in "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(',')]


async def main():
    vm = VM(instructions)
    await vm.run()
    # instructions = loadCSVInput()
    # max_output = 0
    # for phases in itertools.permutations([5,6,7,8,9]):
    #     dprint("Phases: ", phases)
    #     machines = [VM(instructions, phase) for phase in phases]
    #
    #     iter = 0
    #     in_out = 0 # first input
    #
    #     while True:
    #         try:
    #             dprint(f"\n*** iter {iter} ***")
    #             for machine in machines:
    #                 in_out = next(machine.run(in_out))
    #             iter += 1
    #         except StopIteration:
    #             break

        # output = await (plane, prog)
        # max_output = max(max_output, in_out)

    # print(f"max output: {max_output}")

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
