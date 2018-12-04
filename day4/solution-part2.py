import datetime

(BEGIN, WAKE, SLEEP) = range(3)


def parse_log(data_in):
    year = int(data_in[1:5])
    month = int(data_in[6:8])
    day = int(data_in[9:11])
    hour = int(data_in[12:14])
    minute = int(data_in[15:17])

    time = datetime.datetime(year, month, day, hour, minute)
    event = None
    guard = None

    parts = data_in.split(' ')
    if (parts[2] == "Guard"):
        event = BEGIN
        guard = int(parts[3][1:])
    elif (parts[2] == "wakes"):
        event = WAKE
    else:
        event = SLEEP

    return (time, event, guard)


with open("input.txt", "rt") as file:
    entries = [parse_log(x) for x in file]
    entries.sort(key=lambda dt: dt[0])

    asleep = {}
    last_started_guard = None
    for x in entries:
        if (x[1] == BEGIN):
            last_started_guard = x[2]
            actions = asleep.get(last_started_guard, [])
            asleep[last_started_guard] = actions
       # elif (x[1] == SLEEP):
       #     asleep[last_started_guard].append(x[0])
       # elif (x[1] == WAKE):
        else:
            asleep[last_started_guard].append(x[0])

    minutes = {}
    for guard in asleep.keys():
        actions = asleep[guard]
        time_asleep = 0
        sleep_chart = [0] * 60
        for i in range(0, len(actions), 2):
            time_asleep += (actions[i+1] - actions[i]).seconds // 60
            for minute in range(actions[i].minute, actions[i+1].minute):
                sleep_chart[minute] += 1

        minutes[guard] = (time_asleep, sleep_chart)

    print(minutes)

    guard_slept_the_most = 0
    max_minutes = 0
    for guard in asleep.keys():
        minute_most_asleep = max(minutes[guard][1])
        if (minute_most_asleep >= max_minutes):
            max_minutes = minute_most_asleep
            guard_slept_the_most = guard

    print("Guard who slept the most:", guard_slept_the_most, max_minutes)
    print(guard_slept_the_most *
          minutes[guard_slept_the_most][1].index(max_minutes))
