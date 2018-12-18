from PIL import Image
from collections import deque, defaultdict


def read_x_range(line):
    parts = line.replace("y=", "").replace(" x=", "").split(',')
    y = int(parts[0])
    x_min, x_max = [int(x) for x in parts[1].replace('..', ' ').split(' ')]
    return y, x_min, x_max


def read_y_range(line):
    parts = line.replace("x=", "").replace(" y=", "").split(',')
    x = int(parts[0])
    y_min, y_max = [int(x) for x in parts[1].replace('..', ' ').split(' ')]
    return x, y_min, y_max


def print_board(board, w, h):
    for y in range(h):
        for x in range(w):
            print(board[x + y * w], end="")
        print()


def render_board(board, w, h, suffx=0):
    im2 = Image.new("RGB", (w*3, h*3))

    # Expand each pixel 3x3 so it's bigger and easier to see.
    pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            ch = board[x+y*w]
            color = (0, 0, 255)
            if ch == '#':
                color = (155, 155, 0)
            elif ch == '.':
                color = (255, 255, 255)

            row.append(color)
            row.append(color)
            row.append(color)
        pixels.extend(row + row + row)

    # This is the 1x1 pixel approach.
    # im2.putdata([(255,255,255) if x in '.' else (155,155,0) if x == '#' else (0,0,255) for x in board])

    im2.putdata(pixels)
    im2.save(f"foo{str(suffx)}.jpg")


clays = []
with open("input.txt", "rt") as file:
    data = file.readlines()
    for line in data:
        if line[0] == 'x':
            x, y_min, y_max = read_y_range(line)
            for y in range(y_min, y_max+1):
                clays.append((x, y))
        else:
            y, x_min, x_max = read_x_range(line)
            for x in range(x_min, x_max+1):
                clays.append((x, y))

    print(clays)

    max_x = max(clays, key=lambda x: x[0])[0] + 1
    min_x = min(clays, key=lambda x: x[0])[0] - 1
    max_y = max(clays, key=lambda x: x[1])[1]
    min_y = min(clays, key=lambda x: x[1])[1]

    w = max_x - min_x + 2
    h = max_y - min_y + 2

    board = ['.'] * w * h

    for c in clays:
        x = c[0] - min_x
        y = c[1] - min_y
        board[x+y*w] = "#"

    # Rather than add a special character spout, just put a down poor
    board[500-min_x] = '|'

    # Start layout
    print_board(board, w, h)

    def flow_down(board, w, h, x, y):
        # flow_water down
        while (y < h and board[x+y*w] in ".|"):
            board[x+y*w] = '|'
            y += 1

        # Ran off the end
        if y >= h:
            return -1, False

        # If we hit a clay then we back up one position
        new_y = (y if board[x+y*w] in "~|" else y-1)
        # Replace the | with a ~ for where we stopped.
        board[x+new_y*w] = '~'
        return new_y, True

    def flow_sideways(board, w, h, x, y, offset):
        # hack, we expect this will be | so convert it to ~. Otherwise if we allow |'s in the check
        # in the while loop then we run off the end when we drop into an already filled one.
        board[x+y*w] = '~'
        # try left
        can_drop = False
        while (board[x+y*w] in ".~" and not can_drop):
            board[x+y*w] = '~'
            x += offset
            can_drop = board[x+(y+1)*w] == '.'
        return x, (can_drop or board[x+y*w] == '|')

    def flow_left(board, w, h, x, y):
        return flow_sideways(board, w, h, x, y, -1)

    def flow_right(board, w, h, x, y):
        return flow_sideways(board, w, h, x, y, 1)

    def remove_tops(board, w, h):
        for y in range(h):
            # scan forwards looking for |~
            x = 0
            while (x < w):
                if board[x+y*w] == '|' and board[x+1+y*w] == '~':
                    x += 1
                    while (board[x+y*w] == '~'):
                        board[x+y*w] = '|'
                        x += 1
                else:
                    x += 1

            # kinda hacky, but scan backweards  looking for ~|
            x = w - 1
            while (x >= 1):
                if board[x+y*w] == '|' and board[x-1+y*w] == '~':
                    x -= 1
                    while (board[x+y*w] == '~'):
                        board[x+y*w] = '|'
                        x -= 1
                else:
                    x -= 1

    # start
    x = 500-min_x
    y = 1
    can_go_down = True
    iteration = 0

    # Start with the initial water spot, for perf track what spouts we have already
    # processed. This is for when a spout pours into an already overflowed 'bucket' we
    # don't want to reflow from there.
    spouts = [(x, y)]
    processed_spouts = set()

    while can_go_down or spouts:

        # End condition: No spout, nothing to do.
        if not spouts:
            break

        # Simulate this spout, unless we've already seen it.
        x, y = spouts.pop()
        if (x, y) in processed_spouts:
            continue

        processed_spouts.add((x, y))

        y, can_go_down = flow_down(board, w, h, x, y)

        add_left_spout = False
        add_right_spout = False
        while can_go_down and not add_left_spout and not add_right_spout:
            # left
            spout_x, add_left_spout = flow_sideways(board, w, h, x, y, -1)
            if add_left_spout:
                spouts.append((spout_x, y))

            # right
            spout_x, add_right_spout = flow_sideways(board, w, h, x, y, 1)
            if add_right_spout:
                spouts.append((spout_x, y))

            # keep
            y -= 1

        # Uncomment for progress
        # if (iteration % 100 == 0):
        #     render_board(board,w,h,iteration)
        #     sum = 0
        #     for y in range(h):
        #         for x in range(w):
        #             sum += 1 if board[x + y * w] in "~|+" and y + min_y <= max_y else 0
        #     print(sum, spouts)
        iteration += 1

    remove_tops(board, w, h)
    render_board(board, w, h, "final")
    #print_board(board, w, h)

    # Solutions are counting the water and dry wells.
    sum = 0
    dry_well_sum = 0
    for y in range(h):
        for x in range(w):
            sum += 1 if board[x + y * w] in "~|+" and y + min_y <= max_y else 0
            dry_well_sum += 1 if board[x + y * w] == '~' else 0

    print("Part 1: ", sum)
    print("Part 2:", dry_well_sum)
