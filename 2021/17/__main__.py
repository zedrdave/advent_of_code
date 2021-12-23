with open('./input.txt', 'r') as f:
    data = f.read()


target_x, target_y = [tuple(int(i) for i in c[2:].split('..'))
                      for c in data[13:].split(', ')]


def try_launch(dx, dy, target_x, target_y):
    pos_x = 0
    pos_y = 0
    max_y = 0
    init_x, init_y = dx, dy

    while pos_x <= max(target_x) and pos_y >= min(target_y):
        #         print(pos_x, pos_y, dx, dy)
        pos_x += dx
        pos_y += dy
        max_y = max(pos_y, max_y)

        if dx > 0:
            dx -= 1
        dy -= 1

        if max(target_x) >= pos_x >= min(target_x) and min(target_y) <= pos_y <= max(target_y):
            #             print("HIT:", pos_x, pos_y, f"| Init: {init_x}, {init_y}")
            #             print("max y:", max_y)
            return True
    return False


hits = 0
for init_x in range(ceil(((8 * min(target_x) + 1)**.5 - 1)/2), max(target_x)+1):
    for init_y in reversed(range(min(target_y)-1, 2000)):
        hits += try_launch(init_x, init_y, target_x, target_y)
#         if hits:
#             break
#     if hit:
#         break

hits
