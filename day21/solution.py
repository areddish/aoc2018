
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
with open("input.txt", "rt") as file:

    print(file.readline())
    lines = file.readlines()
    for line in lines:
        l = line.strip().split(' ')
        sample_program.append([l[0]] + [int(x) for x in l[1:]])

print("Running...")
registers = [0, 0, 0, 0, 0, 0]
iter = 0
ip = 0

registers[0] = 0 
m = 5e6
seen = set()
while (ip < len(sample_program)):
    ip = registers[1]
    statement = sample_program[ip]
    #print (*registers, ip,":",*statement, end="")
    operations[statement[0]](registers, *statement[1:])
    #print (*registers)
    ip = registers[1] + 1
    registers[1] = ip
    if (ip == 28):
        print("r4: ", registers[4])
        print("Part 1", registers[4])
        if (registers[4] in seen):
            print ("Part 2", m)
            exit(-1)
        seen.add(registers[4])
        m = min(m, registers[4])
        print("p2", registers[4], m)
     #   exit(-1)
print(registers[0])
