lines = [l.strip().split(',') for l in open("input.txt", "r").readlines()]
paths = [[(w[0], int(w[1:])) for w in l] for l in lines]

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x},{self.y})"

def path_to_segments(path):
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

(ls1, ls2) = [path_to_segments(p) for p in paths]

def is_vert(s):
    return s[0].x == s[1].x

def segs_intersect(s1, s2):
    # assume s1 is horiz and s2 is vertical and both positives:
    if is_vert(s1):
        s1, s2 = s2, s1
    if s1[0].x > s1[1].x:
        s1 = [s1[1],s1[0]]
    if s2[0].y > s2[1].y:
        s2 = [s2[1],s2[0]]
    if s1[0].x < s2[0].x and s1[1].x > s2[0].x and \
        s1[0].y > s2[0].y and  s1[0].y < s2[1].y:
        return [Point(s2[0].x, s1[0].y)]
    else:
        return []

intersections = []
for s1 in ls1:
    for s2 in ls2:
        print(f"{s1} {s2}")
        if is_vert(s1) == is_vert(s2):
            continue
        intersections += segs_intersect(s1, s2)


print("Intersections: ", intersections)
dists = [abs(p.x)+abs(p.y) for p in intersections]
print("L1 dists: ", dists)
print("Min L1 dist: ", min(dists))
