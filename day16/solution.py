
import collections

# def regOp(register,a,b,c,op):
#     registers[c] = op(a,b)

# def regOp(register,a,b,c,op):
#     registers[c] = op(registers[a],[b])


def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    registers[c] = registers[a] | b


def setr(registers, a, b, c):
    registers[c] = registers[a]


def seti(registers, a, b, c):
    registers[c] = a


def gtir(registers, a, b, c):
    registers[c] = 1 if a > registers[b] else 0


def gtri(registers, a, b, c):
    registers[c] = 1 if registers[a] > b else 0


def gtrr(registers, a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0


def eqir(registers, a, b, c):
    registers[c] = 1 if a == registers[b] else 0


def eqri(registers, a, b, c):
    registers[c] = 1 if registers[a] == b else 0


def eqrr(registers, a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0


operations = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr
}

before = []
code = []
after = []

sample_program = []

with open("test.txt", "rt") as file:

    while(file):
        b = file.readline()
        if (not "Before:" in b):
            # Done with part 1
            break
        c = file.readline()
        a = file.readline()
        skip = file.readline()
        if not skip == "":
            assert True

        before.append([int(x) for x in b.replace(
            "Before: [", "").replace("]", "").split(',')])
        # opcode input A input b output c
        code.append([int(x) for x in c.split(' ')])
        after.append([int(x) for x in a.replace(
            "After:  [", "").replace("]", "").split(',')])

    print(file.readline())
    lines = file.readlines()
    for line in lines:
        l = line.strip()
        sample_program.append([int(x) for x in line.split(' ')])

counter = 0
possibles = collections.defaultdict(set)

for x in range(len(before)):
    match_count = 0
    for name in operations:
        op = operations[name]
        registers = before[x].copy()
        op(registers, *code[x][1:])
        if (registers == after[x]):
            match_count += 1
            possibles[code[x][0]].add(name)
    if (match_count >= 3):
        counter += 1

print("p1: ", counter)

opcode_mapping = {}
while(len(opcode_mapping) < len(operations)):
    # Find a list with a single and assign that the opcode mapping
    found_op_code = -1
    found_op_code_name = ""
    for x in possibles:
        #        print (x,possibles[x])
        if (len(possibles[x]) == 1):
            found_op_code = x
            found_op_code_name = possibles[x].pop()
            break

    for x in possibles:
        if (found_op_code_name in possibles[x]):
            possibles[x].remove(found_op_code_name)

    opcode_mapping[found_op_code] = operations[found_op_code_name]

print("-" * 51)
print(opcode_mapping)

print("Running...")
registers = [0, 0, 0, 0]
for statement in sample_program:
    opcode_mapping[statement[0]](registers, *statement[1:])

print(registers[0])
