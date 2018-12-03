twos = 0
threes = 0

with open("input.txt", "rt") as file:
    words = file.readlines()
    print("Found", len(words), "words")
    for word in words:
        chars = {}
        for ch in word:
            chars[ch] = chars.get(ch, 0) + 1

        has_twos = False
        has_threes = False
        for x in chars:
            has_twos = has_twos or chars[x] == 2
            has_threes = has_threes or chars[x] == 3
            if (has_twos and has_threes):
                break
        twos += 1 if has_twos else 0
        threes += 1 if has_threes else 0

print(twos*threes)
