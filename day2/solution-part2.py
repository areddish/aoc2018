def diff(a, b):
    c = 0
    position = -1
    for i in range(len(a)):
        if (a[i] != b[i]):
            c += 1
            position = i
        if (c > 1):
            return False, -1

    return c == 1, position


with open("input.txt", "rt") as file:
    words = file.readlines()
    words = [w.strip() for w in words]
    for x in range(len(words)-1):
        a = words[x]
        for y in range(x+1, len(words)):
            b = words[y]
            match, position = diff(a, b)
            if (match):
                print(words[x][:position] + words[x][position+1:])
