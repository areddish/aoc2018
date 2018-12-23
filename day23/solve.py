with open("input.txt", "rt") as file:
    data = []
    lines = file.readlines()

    strongest_r = -1
    strongest_i = -1
    for line in lines:
        line = line.replace("pos=<","").replace(">,",",").replace(" r=","")
        vals = [int(x) for x in line.split(',')]
        data.append(vals)
        if vals[3] > strongest_r:
            strongest_r = vals[3]
            strongest_i = len(data) - 1

    def dist(x,y,z,a,b,c):
        return abs(x-a) + abs(y-b) + abs(z-c)

    def in_range(x,y,z,r):
        in_count = 0
        for i in range(len(data)):
            a,b,c,d = data[i]
            dd = dist(x,y,z,a,b,c)
            if (dist(x,y,z,a,b,c) <= r):
                in_count += 1

        return in_count

    x,y,z,r = data[strongest_i]
    print ("part 1: ", in_range(x,y,z,r))
    
    print("minr = ", min(data, key=lambda x:x[3])[3])
    m = 0
    mi = 0
    for i in range(len(data)):
        inrange = in_range(*data[i])
        if (inrange > m):
            m = inrange
            mi = i

    sx,sy,sz, ignore = data[mi]
    for dy in range(-1000, 1000, 100):
        for dx in range(-1000, 1000, 100):
            for dz in range(-1000, 1000, 100):
                print(dz,dx,dy)
                for i in range(len(data)):
                    inrange = in_range(sx + dx, sy + dy, sz + dz, data[i][3])
                    if (inrange > m):
                        m = inrange
                        print("max",sx+dx,sy+dy,sz+dz, dist(0,0,0,sx+dx,sy+dy,sz+dz))

    print ("part 2:" , m, mi, *data[mi], sx, sy, sz)