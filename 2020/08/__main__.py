from ..utils import input_file

𝓟 = [(l[:3], int(l[4:])) for l in open(input_file())]

def run(P, IP = 0):
    𝒜 = 0
    ℮ = set()
    while 0 <= IP < len(P):
        ℮.add(IP)
        𝒾, a = P[IP]
        if 𝒾 == 'jmp':
            IP += a-1
        if 𝒾 == 'acc':
            𝒜 += a
        IP += 1
        if IP in ℮:
            return False, 𝒜
    return IP == len(P), 𝒜

print('Part 1:', run(𝓟)[1])

for l,(𝒾,a) in enumerate(𝓟):
    if 𝒾 == 'jmp':
        𝒾 = 'nop'
    elif 𝒾 == 'nop':
        𝒾 = 'jmp'
    b,𝒜 = run(𝓟[:l] + [(𝒾,a)] + 𝓟[l+1:])
    if b:
        break

print('Part 2:', 𝒜)


#################################
#
#  Graph resolution
#
#################################

import networkx as nx

𝓟 = [(l[:3], int(l[4:])) for l in open('08/input.txt')]

G = nx.DiGraph([n, n+(a if cmd == 'jmp' else 1), {'acc': (a if cmd == 'acc' else 0)}]
               for n,(cmd,a) in enumerate(𝓟))

cycle = nx.find_cycle(G, 0)
print('Part 1:', nx.shortest_path_length(G, 0, cycle[-1][0], 'acc'))

T = len(𝓟)
nx.set_node_attributes(G, {n: {'i': a} for n, a in enumerate(𝓟)})
for s,t in cycle:
    cmd, a = G.nodes[s]['i']
    nt = s + {'jmp': 1, 'nop': a, 'acc': 0}[cmd]
    if nx.has_path(G, nt, T):
        G.remove_edge(s, t)
        G.add_edge(s, nt, a=0)
        break

print('Part 2:', nx.shortest_path_length(G, 0, T, 'acc'))


###################################
#
# Graph Viz
#
###################################

# d = 14
# import matplotlib.pyplot as plt
# plt.figure(figsize=(10,10))
#
# before = nx.shortest_path(G, 0, cy[-1][0])
# after = max(nx.shortest_path(G, None, T).values(), key=len)
#
# all_nodes = before + list(after)
# layout = {n: (i%d if (i//d)%2 == 0 else d-(i%d)-1, -(i+1)//d) for i,n in enumerate(all_nodes)}
#
# nx.draw(G.subgraph(all_nodes), layout, with_labels=True, node_size=800)
