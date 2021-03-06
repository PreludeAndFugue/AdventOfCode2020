#!python3

from collections import defaultdict, namedtuple
from itertools import product
import re

INPUT = 'day14.txt'
TEST_INPUT_1 = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''
TEST_INPUT_2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''

class Mask(object):
    def __init__(self, mask):
        self.mask = mask


    def apply(self, value):
        '''Part 1.'''
        value = value | self._one_mask
        value = value & self._zero_mask
        return value


    def addresses(self, address):
        '''Part 2.'''
        inital_mask = self.mask.replace('X', '1')
        inital_mask = int(inital_mask, 2)
        address = address | inital_mask
        address = format(address, '0>36b')

        x_count = self.mask.count('X')
        temp_mask = ''.join(m if m == 'X' else a for (m, a) in zip(self.mask, address))
        temp_mask = temp_mask.replace('X', '{}')

        addresses = []
        for z in product('01', repeat=x_count):
            new_address = temp_mask.format(*z)
            addresses.append(''.join(new_address))
        return [int(a, 2) for a in addresses]


    @property
    def _one_mask(self):
        return int(''.join('1' if x == '1' else '0' for x in self.mask), base=2)


    @property
    def _zero_mask(self):
        return int(''.join('0' if x == '0' else '1' for x in self.mask), base=2)


Memory = namedtuple('Memory', ['address', 'value'])

MEM = re.compile(r'^mem\[(\d+)\] = (\d+)$')


def get_input(input):
    for line in input.strip().split('\n'):
        if line.startswith('mask'):
            m = line.split(' = ')[1]
            yield Mask(m)
        elif line.startswith('mem'):
            match = re.match(MEM, line)
            address, value = list(map(int, match.groups()))
            yield Memory(address, value)
        else:
            raise IOError(line)


def work(instructions, helper):
    '''Main algorithm for parts 1 and 2.'''
    memory = defaultdict(int)
    mask = None
    for instruction in instructions:
        if isinstance(instruction, Mask):
            mask = instruction
        elif isinstance(instruction, Memory):
            helper(instruction, mask, memory)
        else:
            raise IOError
    return sum(v for v in memory.values())


def _part1_helper(instruction, mask, memory):
    value = mask.apply(instruction.value)
    memory[instruction.address] = value


def test1(instructions):
    assert work(instructions, _part1_helper) == 165


def part1(instructions):
    return work(instructions, _part1_helper)


def _part2_helper(instruction, mask, memory):
    addresses = mask.addresses(instruction.address)
    for address in addresses:
        memory[address] = instruction.value


def test2(instructions):
    assert work(instructions, _part2_helper) == 208


def part2(instructions):
    return work(instructions, _part2_helper)


def main():
    test_instructions_1 = get_input(TEST_INPUT_1)
    test_instructions_2 = get_input(TEST_INPUT_2)
    instructions = list(get_input(open(INPUT, 'r').read()))

    test1(test_instructions_1)

    p = part1(instructions)
    print(p)

    test2(test_instructions_2)

    p = part2(instructions)
    print(p)


if __name__ == "__main__":
    main()
