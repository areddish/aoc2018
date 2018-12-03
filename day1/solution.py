sum = 0
with open("input.txt", "rt") as file:
    for x in file.readlines():
        sum += int(x)
print(sum)