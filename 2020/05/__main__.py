from ..utils import *

    seats = [l.strip() for l in open(input_file()).readlines()]

    seat_ids = [sum(2**i * (1 if b in ['B','R'] else 0) for i,b in enumerate(s[::-1]))
    for s in seats]

    print("Part 1:", max(seat_ids))

    my_seat = next(seat_id for seat_id in range(2**10) if seat_id not in seat_ids and seat_id+1 in seat_ids and seat_id-1 in seat_ids)

    print("Part 2:", my_seat)
