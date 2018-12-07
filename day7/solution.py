import collections

TEST = ("test.txt", 0, 2)
INPUT = ("input.txt", 60, 5)

INPUT_SET = INPUT


with open(INPUT_SET[0], "rt") as file:
    graph = collections.defaultdict(list)
    step_names = set()
    left = ""
    right = ""
    for line in file:
        parts = line.split(' ')
        first = parts[1]
        before = parts[7]
        graph[before].append(first)
        step_names.add(first)

    # print(graph)

    initial_candidates = set()
    for x in step_names:
        if (x not in graph):
            initial_candidates.add(x)

    print(initial_candidates)

    def can_go(graph, gone):
        candidates = set()
        for x in graph:
            all_gone = sum(
                [1 if child in gone else 0 for child in graph[x]]) == len(graph[x])
            if (all_gone and x not in gone):
                candidates.add(x)
        return candidates

    print("Part 1", "-" * 50)
    visited = set()
    next_candidates = set(initial_candidates)
    while(len(next_candidates) > 0):
        # get the next step
        current_step = min(next_candidates)
        next_candidates.remove(current_step)

        # marked this one has completed
        print(current_step, end="")
        visited.add(current_step)

        # update the list of available next steps based on where we just went
        next_candidates = next_candidates.union(can_go(graph, visited))

    print()

    print("Part 2", "-" * 50)
    def total_time(ch):
        return ord(ch) - 64 + INPUT_SET[1]

    def get_work(next_queue):
        # nothing to do
        if len(next_queue) == 0:
            return ('.', 0), next_queue

        # take work
        next_item = min(next_queue)
        next_queue.remove(next_item)
        return (next_item, total_time(next_item)), next_queue

    def do_work(worker, inprogress, next_queue, visited):
        time_left = worker[1]
        if (time_left <= 1):
            visited.add(worker[0])
            next_queue = next_queue.union(can_go(graph, visited))
            for w in inprogress:
                if (w[0] in next_queue):
                    next_queue.remove(w[0])
            return get_work(next_queue)

        return (worker[0], worker[1]-1), next_queue

    visited = set()
    next_candidates = initial_candidates

    worker_count = INPUT_SET[2]
    workers = []
    for i in range(worker_count):
        worker, next_candidates = get_work(next_candidates)
        workers.append(worker)

    second = 0
    print("Seconds", *[f"Worker {i}" for i in range(worker_count)])
    while(sum([w[1] for w in workers]) > 0):
        assignments = [w[0] for w in workers]
        print(second, *assignments, visited)

        for i in range(worker_count):
            workers[i], next_candidates = do_work(
                workers[i], workers, next_candidates, visited)

        second += 1

    print(second-1)
