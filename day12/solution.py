def advance_generation(state, rules):
    next_gen = ['.'] * len(state)

    # apply the rules
    for rule in rules:
        index = state.find(rule[0])
        while (index != -1):
            next_gen[index+2] = rule[1]
            index = state.find(rule[0], index + 1)

    # add room to grow, could probably be smaller
    return "".join(next_gen) + "...."


def plant_sum(state):
    sum = 0
    for i in range(len(state)):
        sum += (i-6) if state[i] == '#' else 0
    return sum

def no_change(deltas):
    for x in deltas[1:]:
        if (x != deltas[0]):
            return False
    return True


with open("input.txt", "rt") as file:
    data = file.readlines()

    current_state = "......" + data[0].split(' ')[2].strip() + "....."

    rules = []
    for rule in data[2:]:
        parts = rule.split(" => ")
        rules.append((parts[0].strip(), parts[1].strip()))

    # We want this generation
    generation_desired = 5e12

    prev_sum = plant_sum(current_state)
    prev_deltas = [0] * 10
    current_generation = 0
    while (current_generation < generation_desired):
        next_generation = advance_generation(current_state, rules)
        current_generation += 1

        sum = plant_sum(next_generation)

        delta = sum - prev_sum

        # inefficient, but works. should use deque
        prev_deltas.insert(0, delta)
        prev_deltas.pop()

        if (no_change(prev_deltas)):
            # we can solve now
            print(f"Solving after generation: {current_generation} with delta of {delta}")
            print("Part 2 solution:",(generation_desired - current_generation)*delta + sum)
            exit(0)

        prev_sum = sum
        current_state = next_generation

        if (current_generation == 20):
            print(f"Part 1 solution: {plant_sum(current_state)}")
