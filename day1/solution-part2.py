freqs = set()
sum = 0
changes = []
with open("input.txt", "rt") as file:
    changes = [int(x) for x in file.readlines()]

found = False
while(not found):
    for x in changes:
        sum += x
        if (sum in freqs):
            print(sum)
            found = True
            break
        freqs.add(sum)