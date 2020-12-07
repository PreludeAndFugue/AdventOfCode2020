#!python3

from collections import defaultdict
import re

INPUT = 'day07.txt'

TEST_INPUT = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''

PATTERN = r'(\d+)\s(\w+\s\w+)'
BAG = re.compile(PATTERN)


def parse_contents(contents):
    '''
    Parse string of form
        1 bright white bag, 2 muted yellow bags
    to a dict
        {'bright white': 1, 'muted yellow': 2}
    '''
    bags = {}
    for m in re.finditer(PATTERN, contents):
        n = int(m.group(1))
        bags[m.group(2)] = n
    return bags


def get_input(input):
    contains = {}
    for line in input.strip().split('\n'):
        bag, contents = line.split(' contain ')
        bag = bag.rsplit(' ', 1)[0]
        c = parse_contents(contents)
        contains[bag] = c
    return contains


def get_reverse(bags):
    '''Reverses the relationship in `get_input`.'''
    result = defaultdict(list)
    for bag, contents in bags.items():
        for b in contents.keys():
            result[b].append(bag)
    return result


def is_contained_in_count(bag, reverse_bags):
    to_check = reverse_bags[bag]
    seen = set()
    answer = set()
    while to_check:
        item = to_check.pop()
        if item in seen:
            continue
        seen.add(item)
        answer.add(item)
        for b in reverse_bags[item]:
            to_check.append(b)
    return len(answer)


def test1():
    bags = get_input(TEST_INPUT)
    reverse_bags = get_reverse(bags)
    c = is_contained_in_count('shiny gold', reverse_bags)
    assert c == 4


def part1():
    bags = get_input(open(INPUT, 'r').read())
    reverse_bags = get_reverse(bags)
    return is_contained_in_count('shiny gold', reverse_bags)


def main():
    test1()

    p = part1()
    print(p)


if __name__ == "__main__":
    main()
