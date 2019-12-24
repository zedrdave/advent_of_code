import itertools
import asyncio
from collections import deque
import sys
import copy
import itertools
import collections
from enum import IntEnum

from .VM import VM as VMBase
from ..utils import loadCSVInput, dprint, setVerbosity

# Debug:
setVerbosity(True)


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
    def __init__(self, program, label = 'VM', input = stdin, output = stdout):
        self.mem = collections.defaultdict(int)
        for i,d in enumerate(program):
            self.mem[i] = d
        self.RB = 0
        self.IP = 0
        self.input = input
        self.output = output
        self.label = label

    async def run(self):
        while self.mem[self.IP] != OP.HALT:
            dprint(f"{self.label}[{self.IP}] {self.mem[self.IP]}: {self.mem[self.IP+1]} {self.mem[self.IP+2]} {self.mem[self.IP+3]}")

            cmd = self.mem[self.IP] % 100

            if cmd == OP.ADD:
                self.set_param(3, self.param(1) + self.param(2))
                self.IP += 4
            elif cmd == OP.MULT:
                self.set_param(3, self.param(1) * self.param(2))
                self.IP += 4
            elif cmd == OP.INPUT:
                async for val in self.input():
                    input = val
                    break
                else:
                    raise(Exception("Missing input!"))
                dprint(f"{self.label} using input: {input}")
                self.set_param(1, int(input))
                self.IP += 2
            elif cmd == OP.OUTPUT:
                output = int(self.param(1))
                self.IP += 2
                await self.output(output)
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

        dprint(f"{self.label} [HALT]\n")


instructions = [int(i) for i in "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(',')]


class Pipe:
    def __init__(self, init = ()):
        self.buffer = deque(list(init))
        self.cond = asyncio.Condition()

    async def input(self, val):
        async with self.cond:
            print("*** inputting ***")
            self.buffer.append(val)
            self.cond.notify_all()

    async def output(self):
        while True:
            async with self.cond:
                print("*** outputting ***")
                while len(self.buffer) == 0:
                    await self.cond.wait()
                yield self.buffer.popleft()

    def flush(self):
        return [self.buffer.popleft() for _ in range(len(self.buffer))]

# async def prompt(pipe):
#     await pipe.push(stdin())

def join(*pipeIOs):
    async def _joined(val = None):
        for p in pipeIOs:
            print('*** joined')
            if val:
                await p(val)
            else:
                async for i in p():
                    yield i
    return _joined

def constInput(i):
    async def _f():
        while True:
            yield i
    return _f

async def main():

    # vm1 = VM(instructions, input=stdin, output=join(pipe1.input, pipe2.input, stdout)).run()
    # vm2 = VM(instructions, input=pipe1.output, output=join(pipe2.input, stdout)).run()
    # await asyncio.gather(vm1, vm2)
    # print(pipe2.flush())
    #
    # Phases:  (7, 5, 6, 8, 9)
    # using input: 0
    # output: 2
    #
    # output:  2
    # using input: 2
    # output: 4
    #
    # output:  4
    # using input: 4
    # output: 8

    with open('2019/07/input.txt') as f:
        instructions = [int(i.strip()) for i in f.read().split(',')]

    # instructions = loadCSVInput()
    pipe = Pipe([5])
    vm = VM(instructions, label="M1", output=pipe.input)
    vm2 = VM(instructions, label="M2", input=join(pipe.output,stdin))

    # machines = [vm, vm2]
    # await asyncio.gather(vm.run() for vm in machines)
    await asyncio.gather(vm.run(), vm2.run())
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
