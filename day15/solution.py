import collections

(ELF, GOBLIN) = range(2)

class Mob:
    def __init__(self, id, x, y, type):
        self.id = id
        self.hp = 200
        self.damage_dealt = 3
        self.alive = True
        self.type = type
        self.x = x
        self.y = y
        self.path = None

    def attack(self, otherMob):
        print(
            f"ATTACK: {self.id} -> {otherMob.id} {self.x},{self.y} {otherMob.x},{otherMob.y}")
        otherMob.take_damage(self.damage_dealt)
        return otherMob.alive

    def take_damage(self, val):
        self.hp -= val
        if (self.hp <= 0):
            print (f"DIES: {self.id}")
            self.alive = False

    def turn(self, board):
        # can i attack?
        # where to move?
        # can I move?
        pass

    def enemy_type(self):
        return "G" if self.type == ELF else "E"

    def get_marker(self):
        return "E" if self.type == ELF else "G"

    # may not be necessary
    def set_path(self, path):
        self.path = path

    def move(self):
        x = self.x
        y = self.y
        nx = self.path[0][0]
        ny = self.path[0][1]
        print(F"MOVE: {self.id} {x},{y} => {nx},{ny} {self.path}")
        self.path = self.path[1:]
        self.x = nx
        self.y = ny
        return nx, ny


board = []

# manhattan distance


def dist(x, y, x2, y2):
    return abs(x-x2) + abs(y-y2)


def get_path(board, x, y, ex, ey, visited):
    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    paths = []
    for o in offsets:
        nx = x + o[0]
        ny = y + o[1]
        if (str(nx)+","+str(ny) in visited):
            continue
        #print(f"EVAL: get_path {x} {y} => {ex} {ey}  {nx} {ny} {board[nx+ny*w]} {visited}")
        if nx == ex and ny == ey:
            # found it, return empty because we don't actually move to the location
            # print("GOAL!!")
            return []
        if board[nx+ny*w] == '.':
            v = visited.copy()
            v[str(nx)+","+str(ny)] = 1
            #print ("EXPLORE")
            potential_path = get_path(board, nx, ny, ex, ey, v)
            if potential_path != None:
                paths.append([(nx, ny)] + potential_path)

    if len(paths):
        # return one with smallest number of items
        paths.sort(key=lambda p: len(p))
        return paths[0]

    return None


def get_free_attack_spots(board, w, x, y):
    spots = []
    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    for o in offsets:
        nx = x + o[0]
        ny = y + o[1]
        if (board[nx+ny*w] == '.'):
            spots.append((nx, ny))

    return spots


# def find_path_to_enemy(board, w, mob, mobs):
#     enemies = []
#     for m in mobs:
#         if m.id == mob.id or not m.alive:
#             continue
#         if mob.type != m.type:
#             enemies.append(m)

#     free_enemy_spots = []
#     for e in enemies:
#         free = get_free_attack_spots(board, w, e.x, e.y)
#         if len(free) > 0:
#             for spot in free:
#                 free_enemy_spots.append((spot[0], spot[1], e))

#     candidates = [(dist(mob.x, mob.y, targets[0], targets[1]), targets[0], targets[1], targets[2])
#                   for targets in free_enemy_spots]
#     if len(candidates) == 0:
#         return None

#     # sort them in distance order
#     candidates.sort(key=lambda x: x[0])
#     # skip the 0 as it's mob, so take the list after the first
#     for candidate in candidates:
#         #visited = {}
#         #visited[str(mob.x)+","+str(mob.y)] = 1
#         # get_path(board, mob.x, mob.y, candidate[1].x, candidate[1].y, visited)
#         print(f"Finding path {mob.x},{mob.y} to {candidate[3].x},{candidate[3].y}")
#         path = pfind(board, w, h, mob.x, mob.y,
#                         candidate[3].x, candidate[3].y)
#         if path:
#             return path

def find_path_to_enemy(board, w, mob, mobs):
    enemies = []
    for m in mobs:
        if m.id == mob.id or not m.alive:
            continue
        if mob.type != m.type:
            enemies.append(m)

    paths = collections.defaultdict(list)
    for e in enemies:
        path_to_enemy = pfind(board, w, h, mob.x , mob.y, e.x, e.y)
        if (path_to_enemy):
            paths[len(path_to_enemy)].append(path_to_enemy)

    if (len(paths) > 0):
        min_list = paths[min(paths)]
        min_list.sort(key = lambda x: (x[0][1], x[0][0]))
        return min_list[0]

    return None

def my_sort(p):
    p.sort(key=lambda x: x[2], reverse=True)

    # change = True
    # while(change):
    #     change = False
    #     for i in range(len(p)-1):
    #         if p[i][2] == p[i+1][2]:
    #             if (p[i+1][1] > p[i][1] or (p[i+1][1] == p[i][1] and p[i+1][0] > p[i][0])):
    #                 temp = p[i+1]
    #                 p[i+1] = p[i]
    #                 p[i] = temp
    #                 change = True
    return p

def pathfind(board, w, h, x, y, ex, ey):
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)] #(0, -1), (-1, 0), (1, 0), (0, 1)]
    visited = {}
    candidates = collections.deque()
    candidates.append((x, y))
    visited[(x, y, 0)] = True
    paths = []
    path = []
    while(candidates):
        sx, sy = candidates.pop()
        visited[(sx, sy)] = True

        if (len(path) == 0 and not (sx == x and sy == y)):
            path.append((sx,sy))

        subcandidates = []
        for o in offsets:
            nx = sx + o[0]
            ny = sy + o[1]
            if (nx == ex and ny == ey):
                #path.append((ex,ey))
                paths.append((len(path), list(path)))
                continue
            if ((nx, ny) in visited or board[nx+ny*w] != '.'):
                continue
            subcandidates.append((nx, ny, dist(nx, ny, ex, ey)))

        if (len(subcandidates) > 0):
            #subcandidates.sort(key=lambda x: x[2] + x[1] + x[0], reverse=True)
            for sb in my_sort(subcandidates):
                candidates.append((sb[0], sb[1]))
            
            path.append((candidates[-1][0], candidates[-1][1]))
        else:
            if (len(path) > 0):
                path.pop()

    if (len(paths) == 0):
        return []

    paths.sort(key=lambda x: x[0])
    return paths[-1][1]

# def collect(board, w, h, sx, sy, ex, ey):
#     offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

#     possibles = collections.defaultdict(list)
   
#     closed = {}
#     Q = collections.deque()
#     Q.append((ex,ey,0))    
#     while Q:
#         cx, cy, d = Q.pop()

#         closed[(cx,cy)] = True
#         d += 1

#         for x in offsets:
#             nx = cx + x[0]
#             ny = cy + x[1]
            
#             if (nx == sx and ny == sy):
#                 return possibles

#             ch = board[nx + ny * w]
#             if (ch != '.' or (nx,ny) in closed):
#                 continue
    
#             possibles[d].append((nx,ny))
#             Q.append((nx,ny,d))

#     return None

def collect(board, w, h, sx, sy, ex, ey):
    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    possibles = collections.defaultdict(list)
   
    closed = {}
    Q = collections.deque()
    Q.append((ex,ey,0))    
    while Q:
        cx, cy, d = Q.popleft()

        if (cx,cy) in closed:
            continue

        closed[(cx,cy)] = True

        d += 1

        to_append = []
        solved = False
        for x in offsets:
            nx = cx + x[0]
            ny = cy + x[1]
            
            if (nx == sx and ny == sy):
                solved = True
                continue
            ch = board[nx + ny * w]
            if (ch != '.' or (nx,ny) in closed or (nx,ny)in Q):
                continue
    
            if ((nx,ny) not in possibles[d]):
                possibles[d].append((nx,ny))
            to_append.append((nx,ny,d))        

        to_append.sort(key=lambda x: (x[1], x[0]))
        for pt in to_append:
            Q.append(pt)

        if solved:
            x = [d for d in possibles]
            for dist in x:
                if dist >= d:
                    del possibles[dist]
            return possibles

    return None

def build_path(choices, sx, sy, ex, ey):
    if not choices:
        return None

    path = []
    distance = max(choices)
    current = (sx, sy)
    while distance in choices:
        p = choices[distance]
        if len(p) == 1:
            current = p[0]            
            path.append(p[0])
            #return [p[0]]
        else:
            offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
            p.sort(key=lambda x:(x[1],x[0]))
            for option in p:
                if (option in path):
                    continue
                if dist(current[0], current[1], option[0], option[1]) == 1:
                    path.append(option)
                    current = option
                    break
             #       return [desired]
        distance -= 1
    
    return path

# def build_path(choices, sx, sy, ex, ey):
#     if not choices:
#         return None

#     path = []
#     distance = max(choices)
#     current = (sx, sy)
#     while distance in choices:
#         p = choices[distance]
#         if len(p) == 1:
#             current = p[0]
#             path.append(p[0])
#         else:
#             offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
#             for o in offsets:
#                 desired = (current[0] + o[0], current[1] + o[1])
#                 if desired in p and desired not in path:
#                     path.append(desired)
#                     current = desired
#                     break
#         distance -= 1
    
#     return path

def pfind(board, w, h, sx, sy, ex, ey):
    #print(f"FINDING: {sx},{sy} to {ex},{ey}")
    path = build_path(collect(board, w, h, sx, sy, ex, ey), sx, sy, ex, ey)
    # if path:
    #     path.reverse()
    return path

def get_mob_to_attack(board, w, mob, mobs):
    offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    targets = []
    for offset in offsets:
        test_x = mob.x + offset[0]
        test_y = mob.y + offset[1]
        if board[test_x + test_y * w] == mob.enemy_type():
            # find mob with that x/y
            for m in mobs:
                if (m.alive and m.x == test_x and m.y == test_y):
                    targets.append(m)

    if (len(targets) == 0):
        return None

    targets.sort(key=lambda x: (x.y, x.x))
    min_hp = 300
    min_i = 0
    for x in range(len(targets)):
        if targets[x].hp < min_hp:
            min_hp = targets[x].hp
            min_i = x
    return targets[min_i]


def print_board(board, w, h):
    for y in range(0, h):
        for x in range(0, w):
            print(board[x+y*w], end="")


def get_mobs(all_mobs):
    mobs = all_mobs
    mobs.sort(key=lambda m: m.y*w*w+m.x)
    return mobs


with open("input.txt", "rt") as file:
    data = file.readlines()
    x = 0
    y = 0
    w = len(data[0])
    h = len(data)
    print(f"Board is {w}x{h}")
    id = 0
    mobs = []
    for line in data:
        x = 0
        for ch in line:
            if ch == 'E':
                mobs.append(Mob(id, x, y, ELF))
                id += 1
            elif ch == 'G':
                mobs.append(Mob(200+id, x, y, GOBLIN))
                id += 1
            board.append(ch)
            x += 1
        y += 1

    turn = 1

    print(f"-------------------- Start --------------------")
    print_board(board, w, len(data))

    while (True):
        print(f"-------------------- Turn {turn} --------------------")
        mobs.sort(key=lambda m: (m.y, m.x))
        for mob in mobs:
            if not mob.alive:
                print (F"DEAD: {mob.id}")
                continue
            mob_in_attacking_range = get_mob_to_attack(board, w, mob, mobs)
            if (mob_in_attacking_range and mob_in_attacking_range.alive):
                if not mob.attack(mob_in_attacking_range):
                    board[mob_in_attacking_range.x +
                          mob_in_attacking_range.y * w] = '.'
            else:
                # move towards
                find_path = find_path_to_enemy(board, w, mob, mobs)
                if (find_path):
                    mob.set_path(find_path)
                    board[mob.x + mob.y * w] = '.'
                    nx, ny = mob.move()
                    board[nx + ny * w] = mob.get_marker()
                    
                    # see if we can attack after ther move
                    mob_in_attacking_range = get_mob_to_attack(board, w, mob, mobs)
                    if (mob_in_attacking_range and mob_in_attacking_range.alive):
                        if not mob.attack(mob_in_attacking_range):
                            board[mob_in_attacking_range.x +
                                mob_in_attacking_range.y * w] = '.'
                else:
                    print(f"IDLE: {mob.id}")
        for mob in mobs:
            print(f"{mob.id} {mob.type} {mob.x},{mob.y} {mob.hp}")

        goblins_alive = 0
        elves_alive = 0
        hp_sum = 0
        for m in mobs:
            if m.alive:
                goblins_alive += 1 if m.type == GOBLIN else 0
                elves_alive += 1 if m.type == ELF else 0
                hp_sum += m.hp

        print_board(board, w, h)
        print(
             f"GAME OVER: {elves_alive} {goblins_alive} {turn} {hp_sum} {turn * hp_sum}")
        if (goblins_alive == 0 or elves_alive == 0):
            print(
                f"GAME OVER: {elves_alive} {goblins_alive} {turn-1} {hp_sum} {(turn-1) * hp_sum}")
            exit(1)

        turn += 1
       #r = input()

