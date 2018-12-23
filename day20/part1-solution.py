directions = {
    'N': (0, -1),
    'W': (-1, 0),
    'E': (1, 0),
    'S': (0, 1),
}

DOOR_EW = '|'
DOOR_NS = '-'
WALL = '#'
ROOM = '.'
UNKONWN = '?'


def add_room(board, x, y):
    w = 1000
    DOOR_OFFSETS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    WALL_OFFSETS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

    board[x + y * 1000] = '.'
    for do in DOOR_OFFSETS:
        nx = x + do[0]
        ny = y + do[1]
        if (not board[nx + ny * w] in '|-'):
            board[nx + ny * w] = '?'

    for do in WALL_OFFSETS:
        nx = x + do[0]
        ny = y + do[1]
        board[nx + ny * w] = '#'


def fill_path(board, ch, loc):
    sx, sy = loc
    dx, dy = directions[ch]
    sx += dx
    sy += dy
    door_code = '-' if (ch in 'NS') else '|'
    if (not board[sx + sy * 1000] in '|-'):
        board[sx + sy * 1000] = door_code
    sx += dx
    sy += dy
    add_room(board, sx, sy)
    return (sx, sy)


def fill_walls(board):
    return [ch if ch != '?' else '#' for ch in board]


def explore(board, loc):

    size = 0
    start = [(loc[0], loc[1], size)]
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
        DOOR_OFFSETS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for x in DOOR_OFFSETS:
            nx = current[0] + x[0]
            ny = current[1] + x[1]
            if (board[nx + ny * 1000] in "-|"):
                start.append((nx + x[0], ny + x[1], current[2] + 1))
                #assert board[nx+x[0]+(ny+x[1])*1000] == '.' or board[nx+x[0]+(ny+x[1])*1000] == 'X'
                #board[nx+x[0]+(ny+x[1])*1000] = current[2]+1
                max_size = max(max_size, current[2] + 1)

    return max_size


def printb(board, w, h):
    for y in range(500 - h, 500 + h):
        for x in range(500 - w, 500 + w):
            print(board[x + y * 1000], end="")
        print()


def fill_out_board(s, start, board):
    i = 0
    current_loc = start
    stack = []
    while i < len(s):
        ch = s[i]
        if (ch == '('):
            stack.append(current_loc)
        elif (ch == ')'):
            current_loc = stack.pop()
        elif (ch == '|'):
            current_loc = stack[-1]
        else:
            current_loc = fill_path(board, ch, current_loc)
        i += 1


if __name__ == "__main__":
    with open("input.txt", "rt") as file:
        test = file.read().strip()

        test_cases = [
            ("^ENWWW(NEEE|SSE(EE|N))$", 10),
            ("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
            ("^WNE$", 3),
            ("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
            ("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
            (test, -1)
        ]

        for test in test_cases:
            board = [' '] * 1000 * 1000
            start = (500, 500)
            add_room(board, start[0], start[1])
            board[start[0] + start[1] * 1000] = 'X'

            fill_out_board(test[0][1:-1], start, board)
            printb(board, 20, 20)
            board = fill_walls(board)

            print(test[0], explore(board, start) - 1, test[1])
