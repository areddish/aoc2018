with open("input.txt", "rt") as file:
    rects = []
    for claim in file:
        # 1 @ 1,3: 4x4
        claim = claim.replace("#", "").replace(
            ":", "").replace(",", " ").replace("x", " ")
        parts = claim.split(' ')
        id = int(parts[0])
        x = int(parts[2])
        y = int(parts[3])
        w = int(parts[4])
        h = int(parts[5])
        rects.append((id, x, y, w, h))

    # a <= b < c
    def in_range(a, b, c):
        return a <= b and b < c

    def has_overlap(id1, x1, y1, w1, h1, id2, x2, y2, w2, h2):
        equal = x1 == y1 and x2 == y2 and w1 == w2 and h2 == h1
        if (equal):
            return True

        x_in_range = in_range(x2, x1, x2+w2) or in_range(x2, x1+w1, x2+w2)
        y_in_range = in_range(y2, y1, y2+h2) or in_range(y2, y1+h1, y2+h2)
        if (x_in_range and y_in_range):
            return True

        x2_in_range = in_range(x1, x2, x1+w1) or in_range(x1, x2+w2, x1+w1)
        y2_in_range = in_range(y1, y2, y1+h1) or in_range(y1, y2+h2, y1+h1)
        if (x2_in_range and y2_in_range):
            return True

        return (x_in_range and y2_in_range) or (x2_in_range and y_in_range)

    num_rects = len(rects)
    clear = [True] * num_rects

    for r1 in range(num_rects-1):
        candidate = rects[r1]
        for r2 in range(r1+1, num_rects):
            if (has_overlap(*candidate, *rects[r2])):
                clear[rects[r2][0]-1] = False
                clear[candidate[0]-1] = False

    print("Claim #", clear.index(True) + 1)

    # Validation
    count_clear = 0
    for x in clear:
        if (x):
            count_clear += 1

    if count_clear > 1:
        print("Invalid run")
