from aocd import get_data, submit

day = 6
year = 2022
data = get_data(day=day, year=year)


for part, marker_len in ((1, 4), (2, 14)):
    print(f"Part {part}:", next(i for i in range(marker_len, len(data))
                                if len(set(data[i-marker_len:i])) == marker_len))
