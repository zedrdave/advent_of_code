from functools import reduce
with open('./input.txt', 'r') as f:
    data = f.read()

# data = '9C0141080250320F1802104A08'

bdata = bin(int(data, 16))[2:]
bdata = (4 - len(bdata)) % 4 * '0' + bdata


def parse_packets(bdata, max_packets=-1):
    packets = []

    while len(bdata) and any(b for b in bdata if b != '0') and len(packets) != max_packets:
        version, packet_id = int(bdata[:3], 2), int(bdata[3:6], 2)
        bdata = bdata[6:]
#         print(f"version: {version} | packet_id: {packet_id}")
        packet = {'version': version, 'packet_id': packet_id}

        if packet_id == 4:
            num = ''
            for idx in range(0, len(bdata), 5):
                bit_prefix = bdata[0]
                num += bdata[1:5]
                bdata = bdata[5:]
                if bit_prefix == '0':
                    break

#             print('## literal:', int(num, 2))
            packet['val'] = int(num, 2)
        else:
            length_type_id = bdata[0]
            bdata = bdata[1:]

            if length_type_id == '1':
                subpackets_num = int(bdata[:11], 2)
                bdata = bdata[11:]
#                 print('num subpackets:', subpackets_num)
                packet['subpackets'], bdata = parse_packets(
                    bdata, subpackets_num)
            else:
                subpackets_len = int(bdata[:15], 2)
                bdata = bdata[15:]
#                 print('subpackets length:', subpackets_len)
                packet['subpackets'], _ = parse_packets(bdata[:subpackets_len])
                bdata = bdata[subpackets_len:]

            vals = [p['val'] for p in packet['subpackets']]

            if packet_id == 0:
                packet['val'] = sum(vals)
            elif packet_id == 1:
                packet['val'] = reduce(lambda a, b: a*b, vals)
            elif packet_id == 2:
                packet['val'] = min(vals)
            elif packet_id == 3:
                packet['val'] = max(vals)
            elif packet_id == 5:
                assert len(vals) == 2
                packet['val'] = 1 if vals[0] > vals[1] else 0
            elif packet_id == 6:
                assert len(vals) == 2
                packet['val'] = 1 if vals[0] < vals[1] else 0
            elif packet_id == 7:
                assert len(vals) == 2
                packet['val'] = 1 if vals[0] == vals[1] else 0

        packets += [packet]
#         print("bdata left:",len(bdata))
#     if len(bdata):
#         print("Leftover:", bdata)

    return packets, bdata


tree, _ = parse_packets(bdata)


def recur(tree, fn):
    return [fn(tree)] + [x for subtree in tree.get('subpackets', []) for x in recur(subtree, fn)]


print('Part 1:', sum(recur(tree[0], lambda t: t['version'])))
print('Part 2:', tree[0]['val'])
