GROUND = '.'
TREE = '|'
LUMBERYARD = '#'

OFFSETS = [(-1, -1), (0, -1), (1, -1),
           (-1, 0),         (1, 0),
           (-1, 1), (0, 1), (1, 1)]


def count(b, w, h, x, y):
    tree_count = 0
    lumberyard_count = 0
    for offset in OFFSETS:
        nx = x + offset[0]
        ny = y + offset[1]
        if nx >= w or nx < 0 or ny >= h or ny < 0:
            continue
        if b[nx+ny*w] == TREE:
            tree_count += 1
        elif b[nx+ny*w] == LUMBERYARD:
            lumberyard_count += 1
    return tree_count, lumberyard_count


def print_board(board, w, h):
    for y in range(h):
        for x in range(w):
            print(board[x + y * w], end="")
        print()


board = []

with open("input.txt", "rt") as file:
    data = file.readlines()
    for line in data:
        for ch in line:
            board.append(ch)

    h = len(data)
    w = len(data[0])

    for i in range(1000000000):
        new_board = board.copy()

        for y in range(h):
            for x in range(w):
                tree_count, lumberyard_count = count(board, w, h, x, y)
                index = x+y*w

                type = board[index]
                if type == GROUND:
                    if (tree_count >= 3):
                        new_board[index] = TREE
                if type == TREE:
                    if (lumberyard_count >= 3):
                        new_board[index] = LUMBERYARD
                if type == LUMBERYARD:
                    if tree_count >= 1 and lumberyard_count >= 1:
                        new_board[index] = LUMBERYARD
                    else:
                        new_board[index] = GROUND

        # Part 1
        if i == 9:
            trees = sum([1 if x == TREE else 0 for x in new_board])
            yards = sum([1 if x == LUMBERYARD else 0 for x in new_board])
            print("Part 1:", trees * yards)

        # Part 2
        # A series of length 28 starts repeating at 474. Compute the lowest iteration
        # we have the original occurence. First we account for the non repeating numbers. 
        #   offset = desired - 474 + 1   (0->1 based) 
        # Then from this offset we can mod by the series length to get the 'index' into the
        # repeating series. If we add that to the start of the series we get:
        #  474 + ((1000000000 - 474 + 1) % 28) == 495
        if i == 495:        
            trees = sum([1 if x == TREE else 0 for x in new_board])
            yards = sum([1 if x == LUMBERYARD else 0 for x in new_board])
            print("Part 2:", trees * yards)
            exit(-1)
        board = new_board