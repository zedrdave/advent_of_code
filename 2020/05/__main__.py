from ..utils import *

seats = [l.strip() for l in open(input_file()).readlines()]

seat_ids = [sum(2**i * (1 if b in ['B','R'] else 0) for i,b in enumerate(s[::-1]))
for s in seats]

print("Part 1:", max(seat_ids))

my_seat = next(seat_id+1 for seat_id in seat_ids if seat_id+1 not in seat_ids and seat_id+2 in seat_ids)

print("Part 2:", my_seat)
