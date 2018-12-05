import time

def react(polymer):
    stack = []
    for ch in polymer:
        if len(stack) == 0 or abs(stack[-1] - ord(ch)) != 32:
            stack.append(ord(ch))
        else:
            stack.pop()

    return len(stack)

with open("input.txt", "rt") as file:
    polymer = file.read()

    print ("Part #1","-"*25)
    print(react(polymer))

    print ("Part #2","-"*25)
    start = time.time()
    result = []
    for x in range(26):
        ch_upper = chr(65+x)
        ch_lower = chr(65+x).lower()

        test = polymer.replace(ch_upper,'').replace(ch_lower,'')

        result.append(react(test))

    print (min(result), time.time()-start)