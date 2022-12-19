from aocd import get_data, submit
import numpy as np
import sys
import itertools
from collections import defaultdict, Counter
import re

day = 19
year = 2022

data = get_data(day=day, year=year)

#


def explore(minute, stocks, robots, costs, max_minutes):

    global visited

    if minute == max_minutes:
        return (stocks, robots)

    # Heuristic 1: aggregate any resource count that is above max ability to spend
    key_stocks = tuple(
        sys.maxsize if (s + (max_minutes - minute) * r > (max_minutes -
                        minute) * max(c[material] for c in costs)) else s
        for material, (s, r) in enumerate(zip(stocks[:-1], robots[:-1]))
    ) + (stocks[3],)
    prev_min = visited.get((key_stocks, robots), max_minutes + 1)
    if prev_min <= minute:
        return ((-1, -1, -1, -1), (0, 0, 0, 0))
    visited[(key_stocks, robots)] = minute

    make_robots = [(robot, robot_costs) for robot, robot_costs in reversed(list(enumerate(costs)))
                   if all(s >= c for s, c in zip(stocks, robot_costs))]

    # Heursistic 2: build geode crushers whenever possible
    if len(make_robots) > 0 and make_robots[0][0] == 3:
        make_robots = [r for r in make_robots if r[0] == 3]

    # Heuristic 3: if can build geode or obsidian, do not skip
    if len(make_robots) == 0 or make_robots[0][0] < 2:
        make_robots.append((4, (0, 0, 0)))

    solutions = [explore(
        minute=minute + 1,
        stocks=tuple(s + r - c for s, r,
                     c in zip(stocks, robots, robot_costs + (0,))),
        robots=tuple(r + 1 if i == robot else r for i, r in enumerate(robots)),
        costs=costs,
        max_minutes=max_minutes)
        for robot, robot_costs in make_robots]

    return max(solutions, key=lambda x: x[0][-1])


def explore_blueprint(bp, max_minutes):
    global visited
    visited = dict()

    bp_id, ore_c, clay_c, obs_ore_c, obs_clay_c, geodes_ore_c, geodes_obs_c = bp
    costs = ((ore_c, 0, 0), (clay_c, 0, 0), (obs_ore_c, obs_clay_c, 0),
             (geodes_ore_c, 0, geodes_obs_c))
    stocks, _ = explore(0, stocks=(0, 0, 0, 0), robots=(1, 0, 0, 0),
                        costs=costs, max_minutes=max_minutes)

    # print("stocks:", stocks, "robots", robots, " | geodes: ", stocks[-1])

    return (bp_id, stocks[-1])


bps = [list(map(int, re.findall(r"(\d+)", l))) for l in data.split("\n")]

vals = [explore_blueprint(bp, max_minutes=24) for bp in bps]
print("Part 1:", sum(a * b for a, b in vals))

vals = [explore_blueprint(bp, max_minutes=32)[1] for bp in bps[:3]]
print("Part 2:", vals[0] * vals[1] * vals[2])
