import networkx as nx

with open('input.txt', 'r') as f:
    orbits = f.read().splitlines()

G = nx.DiGraph()
G.add_edges_from(orbit.split(')') for orbit in orbits)

# Treat G as undirected:
nx.shortest_path_length(nx.Graph(G), 'SAN', 'YOU') - 1
