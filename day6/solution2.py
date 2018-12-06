with open("input.txt", "rt") as file:
    xs = []
    ys = []
    for line in file:
        parts = line.split(',')
        x = int(parts[0])
        y = int(parts[1])
        xs.append(x)
        ys.append(y)

    y_limit = max(ys)
    x_limit = max(xs)

    def distance(x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)

    print("Part 2", "-"*26)
    points = 0
    for i in range(y_limit):
        for j in range(x_limit):
            dist = 0
            for idx in range(len(xs)):
                dist += distance(i, j, xs[idx], ys[idx])

            if dist < 10000:
                points += 1

    print(points)
