from enum import Enum


class Operators(Enum):
    SUM = 0
    MUL = 1
    MIN = 2
    MAX = 3
    GT = 5
    LT = 6
    EQ = 7


BITS = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

bitstream = ""
pos = 0
with open("16.data") as f:
    for line in f:
        for character in line:
            bitstream += BITS[character]

version_sum = 0


def parse_literal():
    global bitstream, pos
    result_bits = ""
    while bitstream[pos] == "1":
        result_bits += bitstream[pos+1:pos+5]
        pos += 5
    result_bits += bitstream[pos+1:pos+5]
    pos += 5
    print(f"parsed number {int(result_bits, 2)}")
    return int(result_bits, 2)


def parse_operator(packet_type):
    global bitstream, pos
    length_type = bitstream[pos]
    operands = []
    pos += 1
    print(f"operator {length_type=}")
    if length_type == "0":
        num_child_bits = int(bitstream[pos:pos+15], 2)
        pos += 15
        goal_pos = pos + num_child_bits
        while pos < goal_pos:
            p = parse_packet()
            operands.append(p)
        assert pos == goal_pos
    else:
        num_children = int(bitstream[pos:pos+11], 2)
        pos += 11
        print(f"parsing {num_children=}")
        while len(operands) < num_children:
            operands.append(parse_packet())
    op = Operators(packet_type)
    print(f"{op} with {operands}")
    if op == Operators.SUM:
        return sum(operands)
    if op == Operators.MUL:
        result = 1
        for arg in operands:
            result *= arg
        return result
    if op == Operators.MIN:
        return min(operands)
    if op == Operators.MAX:
        return max(operands)
    if op == Operators.GT:
        return 1 if operands[0] > operands[1] else 0
    if op == Operators.LT:
        return 1 if operands[0] < operands[1] else 0
    if op == Operators.EQ:
        return 1 if operands[0] == operands[1] else 0
    assert False


def parse_packet():
    global bitstream, pos, version_sum
    if (len(bitstream)-pos) < 8:
        return None
    version = int(bitstream[pos:pos+3], 2)
    type_id = int(bitstream[pos+3:pos+6], 2)
    print(f"new packet, {version=}")
    version_sum += version
    pos += 6
    if type_id == 4:
        return parse_literal()
    else:
        return parse_operator(type_id)


packets = []
while len(bitstream) - pos > 8:
    print(f"remaining bits: {len(bitstream)-pos}")
    packet = parse_packet()
    if packet is not None:
        packets.append(packet)


print(version_sum)
print(packets)
