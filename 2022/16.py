from pprint import pprint
import matplotlib.pyplot as plt
import networkx as nx
from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re

day = 16
year = 2022

data = get_data(day=day, year=year)


pipes = [re.match(r"Valve (..)[^=]+=(\d+);[a-z ]+([A-Z, ]+)",
                  l).groups() for l in data.split('\n')]

G = nx.Graph()
G.add_edges_from([(s, d) for s, _, dests in pipes for d in dests.split(', ')])
flows = {n: int(w) for n, w, _ in pipes}

assert len(pipes) == len(data.split('\n'))


all_valves = {k for k, v in flows.items() if v}
min_flows = dict()
# nx.bfs_tree(G, 'AA', depth_limit=30)
# print(t)
cur_states = {(('AA', 'AA'), (), 0, ())}
tot_minutes = 26

for minute in range(1, tot_minutes + 1):
    print(
        f"Minute {minute}: max flow = {max([0, *min_flows.values()])} ({len(cur_states)} active states)\n")

    next_states = set()
    for cur_nodes, open_valves, flow, prev_nodes in sorted(cur_states, key=lambda x: x[2], reverse=True):
        flow_rate = sum(flows[n] for n in open_valves)
        flow += flow_rate

        min_flow = flow + flow_rate * (tot_minutes - minute)

        if min_flows.get(cur_nodes, -1) >= min_flow:
            continue

        min_flows[cur_nodes] = min_flow

        if len(open_valves) == len(all_valves):
            continue

        next_states_n = [[], []]
        for i, cur_node in enumerate(cur_nodes):
            next_states_n[i] = [([(next_node, [])
                                 for next_node in G.neighbors(cur_node)
                                 if next_node not in (prev_nodes)]
                                + ([(cur_node, [cur_node])] if flows[cur_node] and cur_node not in open_valves else []))

                                ]
        debug = {(
            tuple(sorted([cur_node1, cur_node2])),
            tuple(sorted(set([*valve1, *valve2, *open_valves]))),
            flow,
            (cur_nodes)
        )
            for cur_node1, valve1 in next_states_n[0]
            for cur_node2, valve2 in next_states_n[1]
        }

        next_states.update(debug)

    cur_states = next_states

    if len(cur_states) == 0:
        print(f"No more moves.")
        break

print(f" Max flow: {max(min_flows.values())}")
