from ..utils import inputFile, dprint

lines = [l.strip().split(',') for l in open(inputFile(), "r").readlines()]
paths = [[(w[0], int(w[1:])) for w in l] for l in lines]

# Wrapper to avoid dealing with confusing p[0]/p[1] all the time:
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x},{self.y})"

def PathToSegments(path):
    segments = []
    cur_pos = Point(0,0)
    for w in path:
        next_pos = Point(cur_pos.x, cur_pos.y)
        if w[0] == 'R':
            next_pos.x += w[1]
        elif w[0] == 'L':
            next_pos.x -= w[1]
        elif w[0] == 'U':
            next_pos.y += w[1]
        elif w[0] == 'D':
            next_pos.y -= w[1]
        else:
            exit(-1)
        segments += [ (cur_pos, next_pos) ]
        cur_pos = next_pos
    return segments

# easier to store and deal with segments than points:
(ls1, ls2) = [PathToSegments(p) for p in paths]

isVertical = lambda s: s[0].x == s[1].x

def SegmentsIntersect(s1, s2):
    # only considering perpendicular intersections:
    if isVertical(s1) == isVertical(s2):
        return False
    # WLOG: s1 horiz, s2 vertical, and both positives:
    if isVertical(s1):
        s1, s2 = s2, s1
    if s1[0].x > s1[1].x:
        s1 = [s1[1],s1[0]]
    if s2[0].y > s2[1].y:
        s2 = [s2[1],s2[0]]
    # check for intersection
    return s1[0].x < s2[0].x < s1[1].x and s2[0].y < s1[0].y < s2[1].y and Point(s2[0].x, s1[0].y)

def L1Dist(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)

intersections = []
step_counts = []
s1_steps = 0

for s1 in ls1:
    s2_steps = 0
    for s2 in ls2:
        inter = SegmentsIntersect(s1, s2)
        if inter:
            intersections += [inter]
            step_counts += [s1_steps + s2_steps + L1Dist(s1[0], inter) + L1Dist(s2[0], inter)]
        s2_steps += L1Dist(*s2)
        # if step_counts and s1_steps + s2_steps > min(step_counts): continue
    s1_steps += L1Dist(*s1)

dprint("Intersections: ", intersections)
dists = [abs(p.x)+abs(p.y) for p in intersections]
dprint("L1 dists: ", dists)
print("Part 1 - Min L1 dist: ", min(dists))
dprint("Step counts: ", step_counts)
print("Part 2 - Min Step count: ", min(step_counts))
