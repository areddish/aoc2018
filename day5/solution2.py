import time

def react(polymer):
    reaction_occured = True
    while (reaction_occured):
        new_polymer = polymer
        for x in range(26):
            seq1 = chr(65+x) + chr(65+x).lower()
            seq2 = chr(65+x).lower() + chr(65+x)

            new_polymer = new_polymer.replace(seq1,'').replace(seq2,'')
        reaction_occured = new_polymer != polymer
        polymer = new_polymer
    return len(polymer)

with open("input.txt", "rt") as file:
    polymer = file.read()

    print ("Part #1","-"*25)
    print (react(polymer))

    print ("Part #2","-"*25)
    start = time.time()
    result = []
    for x in range(26):
        ch_upper = chr(65+x)
        ch_lower = chr(65+x).lower()

        result.append(react(polymer.replace(ch_upper,'').replace(ch_lower,'')))
    print (min(result), time.time()-start)