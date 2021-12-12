import networkx as nx
import functools

with open('input.txt', 'r') as f:
    data = f.read()

G = nx.Graph(l.split('-') for l in data.split('\n'))

# plt.figure(figsize=(10,10))
# nx.draw(G, with_labels=True, node_size=800)


@functools.cache
def count_paths(G, cur_node, visited=frozenset(), bonus_visit=False):
    if cur_node == 'end':
        return 1
    if cur_node in visited:
        if (not bonus_visit or cur_node == 'start'):
            return 0
        bonus_visit = False
    if cur_node[0].islower():
        visited = visited | set([cur_node])

    return sum(count_paths(G, next_node, visited, bonus_visit)
               for next_node in G.neighbors(cur_node))


print('Part 1:', count_paths(G, 'start'))
print('Part 2:', count_paths(G, 'start', bonus_visit=True))
