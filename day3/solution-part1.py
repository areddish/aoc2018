with open("input.txt", "rt") as file:
    rects = []
    for claim in file:
        # 1 @ 1,3: 4x4
        claim = claim.replace(":", "").replace(",", " ").replace("x", " ")
        parts = claim.split(' ')
        x = int(parts[2])
        y = int(parts[3])
        w = int(parts[4])
        h = int(parts[5])
        rects.append((x, y, w, h))

    # Look for overlap by painting the 'fabric'
    fabric = [0 for i in range(1000 * 1000)]

    def paint(fabric, x, y, w, h):
        for i in range(y, y+h):
            row = i * 1000
            for j in range(x, x+w):
                fabric[row + j] = fabric[row + j] + 1

    for r in rects:
        paint(fabric, *r)

    mulitple_claimed_pieces = 0
    for piece in fabric:
        mulitple_claimed_pieces += (1 if piece > 1 else 0)

    print(mulitple_claimed_pieces)
