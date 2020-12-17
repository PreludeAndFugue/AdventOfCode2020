#!python3

from itertools import product

INPUT = 'day17.txt'
TEST_INPUT = '''.#.
..#
###
'''


def get_input(input, dim=3):
    points = {}
    for y, line in enumerate(input.strip().split('\n')):
        for x, el in enumerate(line):
            if dim == 3:
                points[(x, y, 0)] = el
            elif dim == 4:
                points[(x, y, 0, 0)] = el
    return points


def get_neighbour_coords(coord):
    x, y, z = coord
    for dx, dy, dz in product((-1, 0, 1), repeat=3):
        if dx == dy == dz == 0:
            continue
        yield x + dx, y + dy, z + dz


def get_neighbour_coords_4(coord):
    x, y, z, w = coord
    for dx, dy, dz, dw in product((-1, 0, 1), repeat=4):
        if dx == dy == dz == dw == 0:
            continue
        yield x + dx, y + dy, z + dz, w + dw


def get_candidate_coords(points):
    '''Construct a set of coords that are active or neighbours of active coords.'''
    candidates = set()
    candidates.update(points.keys())
    for p in points:
        n = get_neighbour_coords(p)
        candidates.update(n)
    return candidates


def get_candidate_coords_4(points):
    '''Construct a set of coords that are active or neighbours of active coords.'''
    candidates = set()
    candidates.update(points.keys())
    for p in points:
        n = get_neighbour_coords_4(p)
        candidates.update(n)
    return candidates


def count_active_neighbours(coord, points):
    c = 0
    for n in get_neighbour_coords(coord):
        value = points.get(n, '.')
        if value == '#':
            c += 1
    return c


def count_active_neighbours_4(coord, points):
    c = 0
    for n in get_neighbour_coords_4(coord):
        value = points.get(n, '.')
        if value == '#':
            c += 1
    return c


def do_cycle(points):
    candidates = get_candidate_coords(points)
    new_points = {}
    for coord in candidates:
        is_active = points.get(coord, '.') == '#'
        count = count_active_neighbours(coord, points)
        if is_active:
            if count == 2 or count == 3:
                new_points[coord] = '#'
            else:
                new_points[coord] = '.'
        else:
            if count == 3:
                new_points[coord] = '#'
            else:
                new_points[coord] = '.'

    # purge all empty points
    new_points = {k: v for k, v in new_points.items() if v == '#'}

    return new_points


def do_cycle_4(points):
    candidates = get_candidate_coords_4(points)
    new_points = {}
    for coord in candidates:
        is_active = points.get(coord, '.') == '#'
        count = count_active_neighbours_4(coord, points)
        if is_active:
            if count == 2 or count == 3:
                new_points[coord] = '#'
            else:
                new_points[coord] = '.'
        else:
            if count == 3:
                new_points[coord] = '#'
            else:
                new_points[coord] = '.'

    # purge all empty points
    new_points = {k: v for k, v in new_points.items() if v == '#'}

    return new_points


def count_all_active(points):
    return sum(1 if c == '#' else 0 for c in points.values())


def test1():
    p = get_input(TEST_INPUT)
    assert count_all_active(p) == 5

    p = do_cycle(p)
    assert count_all_active(p) == 11

    p = do_cycle(p)
    assert count_all_active(p) == 21

    p = do_cycle(p)
    assert count_all_active(p) == 38

    for _ in range(3):
        p = do_cycle(p)

    assert count_all_active(p) == 112


def part1():
    p = get_input(open(INPUT, 'r').read())
    for _ in range(6):
        p = do_cycle(p)
    return count_all_active(p)


def test2():
    p = get_input(TEST_INPUT, dim=4)
    assert count_all_active(p) == 5

    p = do_cycle_4(p)
    assert count_all_active(p) == 29

    p = do_cycle_4(p)
    assert count_all_active(p) == 60

    for _ in range(4):
        p = do_cycle_4(p)

    assert count_all_active(p) == 848


def part2():
    p = get_input(open(INPUT, 'r').read(), dim=4)
    for _ in range(6):
        p = do_cycle_4(p)
    return count_all_active(p)


def main():
    test1()

    p = part1()
    print(p)

    test2()

    p = part2()
    print(p)


if __name__ == "__main__":
    main()
