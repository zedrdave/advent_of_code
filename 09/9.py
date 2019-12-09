import sys
import copy
import itertools

MEM_SIZE = 10000

class Machine:
    def __init__(self, program, phase = None):
        self.mem = [0]*MEM_SIZE
        for i,d in enumerate(program):
            self.mem[i] = d
        self.RB = 0
        self.IP = 0
        if phase:
            self.set_param(1, phase)
            self.IP += 2

    def run(self, input):
        while self.mem[self.IP] != 99:
            # print(f"[{self.IP}] {self.mem[self.IP]}: {self.mem[self.IP+1]} {self.mem[self.IP+2]} {self.mem[self.IP+3]}")

            cmd = self.mem[self.IP] % 100

            if cmd == 1: # op_add
                self.set_param(3, self.param(1) + self.param(2))
                self.IP += 4
            elif cmd == 2: # op_mult
                self.set_param(3, self.param(1) * self.param(2))
                self.IP += 4
            elif cmd == 3: # op_input
                print(f"using input: {input}")
                self.set_param(1, input)
                self.IP += 2
            elif cmd == 4: # op_output
                output = self.param(1)
                print(f"output: {output}\n")
                self.IP += 2
                # return output
            elif cmd == 5: # op_jump_if_true
                self.IP = self.param(2) if self.param(1) else self.IP+3
            elif cmd == 6: # op_jump_if_false
                self.IP = self.param(2) if not self.param(1) else self.IP+3
            elif cmd == 7: # op_less_than
                self.set_param(3, self.param(1) < self.param(2))
                self.IP += 4
            elif cmd == 8: # op_equals
                self.set_param(3, self.param(1) == self.param(2))
                self.IP += 4
            elif cmd == 9: # op_adjust_RB
                self.RB += self.param(1)
                # print(f"RB: {self.RB}")
                self.IP += 2
            else: # op_err
                print(f"Unknown opcode: {self.mem[self.IP]} ")
                sys.exit(-1)

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


with open("input.txt","r") as f:
    instructions = [int(i.strip()) for i in f.read().split(',')]

# Part 1:
Machine(instructions).run(1)
# 2494485073

# Part 2:
Machine(instructions).run(2)
# 44997
