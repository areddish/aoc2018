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

    fabric = [0 for i in range(1000 * 1000)]
    ownership_infringed = [False] * len(rects)

    def paint(fabric, ownership_infringed, id, x, y, w, h):
        for i in range(y, y+h):
            row = i * 1000
            for j in range(x, x+w):
                # Save any existing ownership info
                existing_id = fabric[row + j]

                # Mark ownership of this piece to latest claim
                fabric[row + j] = id

                # If a claim already exists, mark infringement for both this claim and existing one
                if (existing_id != 0):
                    ownership_infringed[existing_id - 1] = True
                    ownership_infringed[id - 1] = True

    for r in rects:
        paint(fabric, ownership_infringed, *r)

    # claim numbers are 1-based
    single_clear_claim = ownership_infringed.index(False)
    print("Claim #", single_clear_claim + 1)

    # validation, make sure only one False value
    rects_unclaimed = 0
    for x in ownership_infringed:
        if (not x):
            rects_unclaimed += 1
    if (rects_unclaimed != 1):
        print("INVALID: More than one unclaimed rect.")
