import collections

with open("input.txt", "rt") as file:
    xs = []
    ys = []
    for line in file:
        parts = line.split(',')
        x = int(parts[0])
        y = int(parts[1])
        xs.append(x)
        ys.append(y)

    y_limit = max(ys) + 3
    x_limit = max(xs) + 3
    grid = [0] * x_limit * y_limit

    def distance(x1, y1, x2, y2):
        return abs(x2-x1) + abs(y2-y1)

    def xy_to_i(x, y):
        return y*x_limit + x

    def fill(grid, x, y, ch):
        for j in range(y_limit):
            for i in range(x_limit):
                dist = distance(x, y, i, j)
                grid[xy_to_i(i, j)] = (dist, ch if dist != 0 else ch.upper())

    grids = {}
    for i in range(len(xs)):
        grids[i] = [0] * x_limit * y_limit
        fill(grids[i], xs[i], ys[i], chr(ord('a') + i))

    def pretty_print(grid):
        for j in range(y_limit):
            for i in range(x_limit):
                print(grid[xy_to_i(i, j)][1], end="")
            print()

    # for d in range(len(xs)):
    #     pretty_print(grids[d])

    def combine(grid1, grid2):
        for j in range(y_limit):
            for i in range(x_limit):
                idx = xy_to_i(i, j)
                d1 = grid1[idx][0]
                d2 = grid2[idx][0]
                if (d1 == d2):
                    grid1[idx] = (d1, '.')
                elif (d1 < d2):
                    grid1[idx] = (d1, grid1[idx][1])
                else:
                    grid1[idx] = (d2, grid2[idx][1])

    for i in range(1, len(xs)):
        combine(grids[0], grids[i])

    freq = collections.Counter([x[1] for x in grids[0]]).most_common()

    # find the border and exclude those from the solution
    infinite_chs = {}
    for i in range(x_limit):
        infinite_chs[grids[0][xy_to_i(i, 0)][1]] = True
        infinite_chs[grids[0][xy_to_i(i, y_limit-1)][1]] = True
    for j in range(y_limit):
        infinite_chs[grids[0][xy_to_i(0, j)][1]] = True
        infinite_chs[grids[0][xy_to_i(x_limit-1, j)][1]] = True

    print("Part 1", "-"*26)
    for ch, count in freq:
        if (ch in infinite_chs):
            continue
        print(count+1)
        exit(0)
