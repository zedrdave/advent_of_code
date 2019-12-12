import networkx as nx

with open('input.txt', 'r') as f:
    orbits = f.readlines()

G = nx.DiGraph()
for p1,p2 in [orbit.strip().split(')') for orbit in orbits]:
    # p1 in G.nodes or G.add_node(p1)
    # p2 in G.nodes or G.add_node(p2)
    G.add_edge(p2, p1)

sum(map(lambda node: len(nx.descendants(G, node)), G.nodes))

# 122782
