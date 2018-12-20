board = []

directions = {
    'N' : (0,-1),
    'W' : (-1, 0),
    'E': (1, 0),
    'S' : (0,1),
}

DOOR_EW = '|'
DOOR_NS = '-'
WALL = '#'
ROOM = '.'
UNKONWN = '?'


def parse_path(re):
    paths = []
    i = 0
    while i < len(re) and re[i] != '$':

        if '(' in re:
            next_branch = re.index('(')
            closing_branch = re.rindex(')')

            paths.append(re[:next_branch])
            paths.append(parse_path(re[next_branch+1:closing_branch]))
        
            re = re[closing_branch+1:]
        else:
            paths.append(re[:re.index('$')])
            return paths

    return paths
    
def groups(reg):
    groups = []
    start_path = None
    path = reg
    while '(' in path:
        next_branch = path.index('(')
        closing_branch = path.rindex(')')

        if not start_path:
            start_path = path[:next_branch]

        group = path[next_branch+1:closing_branch]
        
        groups.append(path[next_branch+1:closing_branch])
        path = path[closing_branch+1:]

    return start_path, groups


class Path:
    def __init__(self, path):
        self.children = []
        self.path = path

    def add(self,ch):
        self.path += ch

    def add_child(self, child):
        if (child.path != ""):
            self.children.append(child)

def parse(reg):
    i = 0
    
    (PARSING,IN_GROUP,OPTION) = range(3)

    root = Path("")
    curr_path = Path("")
    group_path = None
    groups = []
    mode = PARSING

    stack = [ root ]
    while (i < len(reg)):
        ch = reg[i]
        if (ch == '('):            
            # start group
            print ("START Group")
            mode = IN_GROUP
            stack.append(curr_path)
            curr_path = Path("")
        elif (ch == ')'):
            # end group
            assert mode == IN_GROUP
            print ("END Group")
            stack[-1].add_child(curr_path)
            curr_path = stack.pop()
                # sibling
                #root.append(curr_path)
                #curr_path = Path("")
        elif (ch == '|'):          
            # add option
            print ("OPTION")
            assert mode == IN_GROUP
            stack[-1].add_child(curr_path)
            curr_path = Path("")
        else:
            curr_path.add(ch)
        i += 1
    if (curr_path.path != ""):
        root.add_child(curr_path)        
    return root


def add_room(board, x, y):
    w = 1000
    DOOR_OFFSETS = [(1,0), (-1,0), (0,-1), (0,1)]
    WALL_OFFSETS = [(-1,-1), (1,1), (-1,1), (1,-1)]
    
    board[x+y*1000] = '.'
    di = 0
    for do in DOOR_OFFSETS:
        nx = x + do[0]
        ny = y + do[1]
        if (not board[nx+ny*w] in '|-'):
            board[nx+ny*w] = '?' #'|' if di <= 1 else '-'
        di += 1

    for do in WALL_OFFSETS:
        nx = x + do[0]
        ny = y + do[1]
        board[nx+ny*w] = '#'


def printb(board, w,h):
    for y in range(500-h, 500+h):
        for x in range(500 -w, 500+w):
            print(board[x+y*1000], end="")
        print ()

def fill_path(board, path, loc):
    doors_passed = 0
    sx, sy = loc
    for x in path:        
        dir = directions[x]
        sx += dir[0]
        sy += dir[1]     
        door_code = '-' if (x in 'NS') else '|'
        if (not board[sx+sy*1000] in '|-'):
            doors_passed += 1
            board[sx+sy*1000] = door_code
        sx += dir[0]
        sy += dir[1]
        add_room(board, sx,sy)
    return sx, sy, doors_passed

def mark_path(board, root, loc):
    nx, ny, door_count = fill_path(board, root.path, loc)
    if len(root.children) == 0:
        return door_count, nx, ny
    
    sizes = []
    for c in root.children:
        s, tx, ty = mark_path(board, c, (nx, ny))
        sizes.append(door_count + s)

    return max(sizes), nx, ny
        
def fill_walls(board):
    return [ch if ch != '?' else '#' for ch in board]

def explore(board, loc):

    size = 0
    start = [ (loc[0], loc[1], size)]
    visited = {}
    max_size = 0
    while len(start) > 0:
        current = start.pop()

        if (current[0], current[1]) in visited:
            #max_size = max(max_size, current[2])
            continue

        # mark it seen
        visited[(current[0], current[1])] = True

        # try each door
        DOOR_OFFSETS = [(1,0), (-1,0), (0,-1), (0,1)]
        for x in DOOR_OFFSETS:
            nx = current[0] + x[0]
            ny = current[1] + x[1]
            if (board[nx+ny*1000] in "-|"):
                start.append((nx+x[0],ny+x[1],current[2]+1))
                #assert board[nx+x[0]+(ny+x[1])*1000] == '.' or board[nx+x[0]+(ny+x[1])*1000] == 'X'
                #board[nx+x[0]+(ny+x[1])*1000] = current[2]+1
                max_size = max(max_size, current[2]+1)

    return max_size
        

def walk(node):
    size = len(node.path)
    if (len(node.children) == 0):
        return size
    return max([size + walk(x) for x in node.children])
        
### RESUE DAY15

with open("input.txt", "rt") as file:
    lines = file.read()
    #lines = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    lines = "^ES(E(E|W)W)"
#    start, groups = groups(lines[1:])
    nodes = parse(lines[1:-1])

    board = [' '] * 1000 * 1000

    start = (500,500)

    add_room(board, start[0], start[1])
    board[start[0]+start[1]*1000] = 'X'
    printb(board, 10,10)

    size = 0
    nx, ny = start
    for root in nodes.children:
        s, nx, ny = mark_path(board, root, (nx, ny))
        size += s
    print ("size: ", size)
    board = fill_walls(board)    

    printb(board, 120,120)
    print ("MAX:",explore(board,start)-1)
    #printb(board, 120,120)

    l = 0
    for root in nodes.children:
        l += walk(root)
    print(l)