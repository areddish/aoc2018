import datetime


def parse_log(data_in):
    year = int(data_in[1:5])
    month = int(data_in[6:8])
    day = int(data_in[9:11])
    hour = int(data_in[12:14])
    minute = int(data_in[15:17])

    time = datetime.datetime(year, month, day, hour, minute)
    guard = None

    parts = data_in.split(' ')
    if (parts[2] == "Guard"):
        guard = int(parts[3][1:])

    return (time, guard)


with open("input.txt", "rt") as file:
    entries = [parse_log(x) for x in file]
    entries.sort(key=lambda dt: dt[0])

    asleep = {}
    last_started_guard = None
    wake = None

    for entry in entries:
        if entry[1]:
            last_started_guard = entry[1]
            actions = asleep.get(last_started_guard, (0, [0]*60))
            asleep[last_started_guard] = actions
            wake = None
        else:
            if (not wake):
                wake = entry[0]
            else:
                minutes_asleep = asleep[last_started_guard][0] + \
                    (entry[0] - wake).seconds // 60
                sleep_chart = asleep[last_started_guard][1]
                for minute in range(wake.minute, entry[0].minute):
                    sleep_chart[minute] += 1
                asleep[last_started_guard] = (minutes_asleep, sleep_chart)
                wake = None


    # This could be rolled into the previous loop but then we wind up doing a lot of comparisons
    # while computing the sleep charts. So do it as a second pass.
    guard_slept_the_most = None
    max_minutes_asleep = 0
    guard_with_single_minute_max = None
    max_single_minutes_asleep = 0

    for guard in asleep.keys():
        if (asleep[guard][0] >= max_minutes_asleep):
            max_minutes_asleep = asleep[guard][0]
            guard_slept_the_most = guard

        minute_most_asleep = max(asleep[guard][1])
        if (minute_most_asleep >= max_single_minutes_asleep):
            max_single_minutes_asleep = minute_most_asleep
            guard_with_single_minute_max = guard

    print("-"*25, "Part 1")
    print("Guard who slept the most:", guard_slept_the_most)
    print(guard_slept_the_most *
          asleep[guard_slept_the_most][1].index(max(asleep[guard_slept_the_most][1])))

    print("-"*25, "Part 2")
    print("Guard who slept the most at a particular minute:", guard_with_single_minute_max,
          "-", max_single_minutes_asleep, "days asleep the same minute")
    print(guard_with_single_minute_max *
          asleep[guard_with_single_minute_max][1].index(max_single_minutes_asleep))
