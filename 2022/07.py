from dataclasses import dataclass, field
from aocd import get_data, submit

day = 7
year = 2022

data = get_data(day=day, year=year)


@dataclass
class Node:
    name: str = None
    parent: 'Node' = None
    children: list = field(default_factory=list)
    size: int = 0

    def compute_size(self):
        self.size += sum(c.compute_size() for c in self.children)
        return self.size

    def size_below(self, threshold):
        if len(self.children):
            ret = self.size if self.size <= threshold else 0
            return ret + sum(c.size_below(threshold) for c in self.children)
        return 0

    def smallest_above(self, threshold):
        if (len(self.children) == 0) or (self.size < threshold):
            return 0
        subs = [c.smallest_above(threshold) for c in self.children]
        subs = [c for c in subs if c]
        if len(subs):
            return min(subs)
        return self.size


root = Node(name='/')
cur_node = root
for inst in data.split("\n")[1:]:
    if inst[0] == '$':
        if inst[2] == 'c':
            if inst[5:7] == '..':
                cur_node = cur_node.parent
            else:
                cur_node = next(
                    child for child in cur_node.children if child.name == inst[5:])
    else:
        size, name = inst.split()
        if size == 'dir':
            size = 0
        cur_node.children.append(
            Node(name=name, size=int(size), parent=cur_node))


root.compute_size()

print("Part 1:", root.size_below(100000))

need_space = 30000000 - (70000000 - root.size)

print("Part 2:", root.smallest_above(need_space))
