### path find
import collections
# Globally used reading order arranged offsets
offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

# LOGGING for visual debugging
VERBOSE_LOGGING = False

def log(msg, **kwargs):
    if (VERBOSE_LOGGING):
        print(msg, **kwargs)
# Get's all reachable locations between (sx,sy)-(ex,ey)
def collect(board, w, h, sx, sy, ex, ey, passable):
    global offsets

    possibles = collections.defaultdict(list)

    closed = {}
    Q = collections.deque()
    Q.append((ex, ey, 0))
    while Q:
        cx, cy, d = Q.popleft()

        # Don't search things we've seen already
        if (cx, cy) in closed:
            continue

        # Mark this seen
        closed[(cx, cy)] = True

        # Increase the cost
        d += 1

        # Check reachable nodes
        to_append = []
        solved = False
        for x in offsets:
            nx = cx + x[0]
            ny = cy + x[1]

            if (nx == sx and ny == sy):
                solved = True
                continue

            if (nx >= w or nx < 0 or ny >=h or ny <0 ):
                continue

            ch = board[nx + ny * w]
            if ((not ch in passable) or (nx, ny) in closed or (nx, ny)in Q):
                continue

            if ((nx, ny) not in possibles[d]):
                possibles[d].append((nx, ny))
            to_append.append((nx, ny, d))

        # Append in reading order
        to_append.sort(key=lambda x: (x[1], x[0]))
        for pt in to_append:
            Q.append(pt)

        # If we found a solution, remove anything larger than current solution.
        if solved:
            x = [d for d in possibles]
            for dist in x:
                if dist >= d:
                    del possibles[dist]
            return possibles

    return None

# Manhattan distance
def dist(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

# Builds a path given available reachable nodes.
def build_path(choices, sx, sy, ex, ey):
    if not choices:
        return 5000, None

    path = []
    distance = max(choices)
    current = (sx, sy)
    while distance in choices:
        p = choices[distance]
        if len(p) == 1:
            current = p[0]
            path.append(p[0])
            # We don't really use the path, just the first item in the path
            return distance, [p[0]]
        else:
            p.sort(key=lambda x: (x[1], x[0]))
            for option in p:
                if (option in path):
                    continue
                if dist(current[0], current[1], option[0], option[1]) == 1:
                    path.append(option)
                    current = option
                    # We don't really use the path, just the first item in the path
                    return distance, [current]
        distance -= 1

### end path find
(ROCKY, WET, NARROW) = range(3)

memo = {}
def get_erosion_level(x,y, depth, tx,ty):

    if (x,y) in memo:
        return memo[(x,y)]
    ans = (get_index(x,y, depth,tx,ty) + depth) % 20183
    memo[(x,y)] = ans
    return ans

def get_index(x,y, depth, tx,ty):
    if x == 0 and y == 0:
        return 0
    if x == tx and y == ty:
        return 0

    if y == 0:
        return x * 16807

    if x == 0:
        return y * 48271
    
    return get_erosion_level(x-1,y, depth,tx,ty) * get_erosion_level(x,y-1, depth, tx, ty)

def get_risk(x,y,depth, tx, ty):
    d = get_erosion_level(x,y,depth, tx, ty) % 3
    if (d == 0):
        return ROCKY
    elif (d == 1):
        return WET
    else:
        return NARROW

# depth = 510 # 10689
# target = (10,10) #*11,722)

depth =  10689
target = (11,722)

risk = 0
for y in range(target[1]+1):
    for x in range(target[0]+1):
        risk += get_risk(x,y,depth, target[0], target[1])

print ("part 1: ", risk)
w = 50
h = 750
parts = ['.','=','|']
board = ['#'] * w * h
for y in range(h):
    for x in range(w):
        board[x+y*w] = parts[get_risk(x,y,depth, target[0], target[1])]

board[0] = 'M'
board[target[0] + target[1] * w] = 'T'

(TORCH, CLIMB, NIETHER) = range(3)

preferred = {
    TORCH: ".|",
    CLIMB : ".=",
    NIETHER: "=|"
}
equipped = TORCH

# current = (0,0)
# n = []
# time = 0
# while current != target:
#     choices = []
#     for o in offsets:
#         nx = current[0] + o[0]
#         ny = current[1] + o[1]
#         if (nx <0 or ny <0 or nx >= w or ny >=h):
#             continue
#         choices.append((nx,ny,1 if board[nx+ny*w] in preferred[equipped] else 8))
    
#     choices.sort(key=lambda x: x[2], reverse=True)
#     #n.extend(choices)
#     time += choices[0][2]
#     current = (choices[0][0], choices[0][1])

c = collect(board, w, h, 0,0, target[0], target[1], ".=|")#preferred[equipped])
print (c)
path = build_path(c,0,0,target[0], target[1])
print("path", path)
