import sys
import copy
import itertools

class Machine:
    def __init__(self, data, phase):
        self.data = copy.deepcopy(data)
        self.IP = 0
        self.set_param(1, phase)
        self.IP += 2

    def run(self, input):
        while self.data[self.IP] != 99:
            # print(f"[{self.IP}] {self.data[self.IP]}: {self.data[self.IP+1]} {self.data[self.IP+2]} {self.data[self.IP+3]}")

            cmd = self.data[self.IP] % 100

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
                return output
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
            else: # op_err
                print(f"Unknown opcode: {self.data[self.IP]} ")
                sys.exit(-1)

        # print("[END]\n")
        return 0

    @property
    def is_running(self):
        return self.data[self.IP] != 99

    def param(self, n):
        if (self.data[self.IP] // (10**(n+1)))%10:
            return self.data[self.IP+n]
        else:
            return self.data[self.data[self.IP+n]]

    def set_param(self, n, val):
        if (self.data[self.IP] // (10**(n+1)))%10:
            self.data[self.IP+n] = val
        else:
            self.data[self.data[self.IP+n]] = val


with open("input.txt","r") as f:
    contents = [int(i.strip()) for i in f.read().split(',')]

max_output = 0

for phases in itertools.permutations([5,6,7,8,9]):
    print("Phases: ", phases)
    machines = [Machine(contents, phase) for phase in phases]

    iter = 0
    in_out = 0 # first input

    while machines[0].is_running:
        print(f"\n*** iter {iter} ***")
        for machine in machines:
            in_out = machine.run(in_out)
        iter += 1
    max_output = max(max_output, in_out)

    print(f"max output: {max_output}")

# 1047153
