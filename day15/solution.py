import collections

# Globally used reading order arranged offsets
offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]

# LOGGING for visual debugging
VERBOSE_LOGGING = False

def log(msg, **kwargs):
    if (VERBOSE_LOGGING):
        print(msg, **kwargs)

# Simple type marker
(ELF, GOBLIN) = range(2)

# Mob class: either elf or goblin
class Mob:
    def __init__(self, id, x, y, type, attack_power):
        self.id = id
        self.hp = 200
        self.damage_dealt = attack_power
        self.alive = True
        self.type = type
        self.x = x
        self.y = y

    def attack(self, otherMob):
        log(f"ATTACK: {self.id} -> {otherMob.id} {self.x},{self.y} {otherMob.x},{otherMob.y}")
        otherMob.take_damage(self.damage_dealt)
        return otherMob.alive

    def take_damage(self, val):
        self.hp -= val
        if (self.hp <= 0):
            log(f"DIES: {self.id}")
            self.alive = False

    def enemy_marker(self):
        return "G" if self.type == ELF else "E"

    def get_marker(self):
        return "E" if self.type == ELF else "G"

    def move(self, new_x, new_y):
        x = self.x
        y = self.y
        log(F"MOVE: {self.id} {x},{y} => {new_x},{new_y}")
        self.x = new_x
        self.y = new_y
        return new_x, new_y

# Got hrough all possible enemies, compute a path to them and pick the shortest in reading order
# TODO: More pruning as there are unreachable mobs we are pathing too repeatedly for nothing.
def find_path_to_enemy(board, w, h, mob, mobs):
    enemies = []
    for m in mobs:
        if m.id == mob.id or not m.alive:
            continue
        if mob.type != m.type:
            enemies.append(m)

    paths = collections.defaultdict(list)
    for e in enemies:
        path_length, path_to_enemy = build_path(collect(board, w, h, mob.x, mob.y, e.x, e.y), mob.x, mob.y, e.x, e.y)
        if (path_to_enemy):
            paths[path_length].append(path_to_enemy)

    if (len(paths) > 0):
        min_list = paths[min(paths)]
        min_list.sort(key=lambda x: (x[0][1], x[0][0]))
        return min_list[0]

    return None

# Get's all reachable locations between (sx,sy)-(ex,ey)
def collect(board, w, h, sx, sy, ex, ey):
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

            ch = board[nx + ny * w]
            if (ch != '.' or (nx, ny) in closed or (nx, ny)in Q):
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

def get_mob_to_attack(board, w, mob, mobs):
    global offsets

    targets = []
    for offset in offsets:
        test_x = mob.x + offset[0]
        test_y = mob.y + offset[1]
        if board[test_x + test_y * w] == mob.enemy_marker():
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
            log(board[x+y*w], end="")


def do_simulation(elf_start_attack, buff_elves):
    elf_attack_power = elf_start_attack
    while(True):
        buff_them = False

        board = []
        with open("input.txt", "rt") as file:
            data = file.readlines()
            x = 0
            y = 0
            w = len(data[0])
            h = len(data)
            log(f"Board is {w}x{h}")
            id = 0
            mobs = []
            for line in data:
                x = 0
                for ch in line:
                    if ch == 'E':
                        mobs.append(Mob(id, x, y, ELF, elf_attack_power))
                        id += 1
                    elif ch == 'G':
                        mobs.append(Mob(200+id, x, y, GOBLIN, 3))
                        id += 1
                    board.append(ch)
                    x += 1
                y += 1

            turn = 0

            log(f"-------------------- Start --------------------")
            print_board(board, w, len(data))

            while (not buff_them):
                log(f"-------------------- Turn {turn} --------------------")
                mobs.sort(key=lambda m: (m.y, m.x))
                for mob in mobs:
                    if not mob.alive:
                        log(F"DEAD: {mob.id}")
                        continue
                    
                    # If something is near, hit it.
                    mob_in_attacking_range = get_mob_to_attack(
                        board, w, mob, mobs)
                    if (mob_in_attacking_range and mob_in_attacking_range.alive):
                        if not mob.attack(mob_in_attacking_range):
                            board[mob_in_attacking_range.x +
                                  mob_in_attacking_range.y * w] = '.'
                    else:
                        # Otherwise go find something to hit.
                        find_path = find_path_to_enemy(board, w, h, mob, mobs)
                        if (find_path):
                            nx, ny = find_path[0]
                            board[mob.x + mob.y * w] = '.'
                            mob.move(nx, ny)
                            board[nx + ny * w] = mob.get_marker()

                            # Turns out we get a chance to hit after we move, use it.
                            mob_in_attacking_range = get_mob_to_attack(
                                board, w, mob, mobs)
                            if (mob_in_attacking_range and mob_in_attacking_range.alive):
                                if not mob.attack(mob_in_attacking_range):
                                    board[mob_in_attacking_range.x +
                                          mob_in_attacking_range.y * w] = '.'
                        else:
                            log(f"IDLE: {mob.id}")

                # HP Dumping for debugging                
                #for mob in mobs:
                #   log(f"{mob.id}: is {mob.get_marker()} @ {mob.x},{mob.y}  HP = {mob.hp}")

                goblins_alive = 0
                elves_alive = 0
                hp_sum = 0
                for m in mobs:
                    if m.alive:
                        goblins_alive += 1 if m.type == GOBLIN else 0
                        elves_alive += 1 if m.type == ELF else 0
                        hp_sum += m.hp
                    else:
                        # Elf down... the humanity. Maybe nerf the goblins next time?
                        if m.type == ELF:
                            buff_them = buff_elves

                print_board(board, w, h)
                # print(
                #     f"GAME OVER: {elves_alive} {goblins_alive} {turn} {hp_sum} {turn * hp_sum}")
                if (goblins_alive == 0 or elves_alive == 0):
                    turn_for_answer = turn 
                    print(
                        f"GAME OVER: Es:{elves_alive} Gs:{goblins_alive} Turn:{turn_for_answer} TotalHP:{hp_sum} Answer:{turn_for_answer * hp_sum}")
                    # Simualation over
                    return

                turn += 1
            #For single stepping w/o debugger.
            #r = input()

        if (buff_elves):
            elf_attack_power += 1
        else:
            # Part 1 solution early termination.
            return


# Part 1
do_simulation(3, False)
# Part 2
do_simulation(4, True)
