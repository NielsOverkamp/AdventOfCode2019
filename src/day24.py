from typing import Set, Tuple, Iterable

from itertools import product, chain

_data = '''.#..#
#..##
##..#
##.##
#..##'''

# _data = '''....#
# #..#.
# #..##
# ..#..
# #....'''

CellMap = Set[Tuple[int, int, int]]


def _neighbours(coord: Tuple[int, int]):
    return iter(map(lambda x: (coord[0] + x[0], coord[1] + x[1]), ((0, 1), (1, 0), (0, -1), (-1, 0))))


def neighbours(coord: Tuple[int, int, int], maxs: Tuple[int, int]) -> Iterable[Tuple[int, int, int]]:
    center = maxs[0] // 2, maxs[1] // 2
    r_iter = None
    if coord[:2] == (center[0] - 1, center[1]):
        r_iter = map(lambda y: (0, y, coord[2] + 1), range(maxs[1] + 1))
    elif coord[:2] == (center[0] + 1, center[1]):
        r_iter = map(lambda y: (maxs[0], y, coord[2] + 1), range(maxs[1] + 1))
    elif coord[:2] == (center[0], center[1] - 1):
        r_iter = map(lambda x: (x, 0, coord[2] + 1), range(maxs[0] + 1))
    elif coord[:2] == (center[0], center[1] + 1):
        r_iter = map(lambda x: (x, maxs[1], coord[2] + 1), range(maxs[0] + 1))
    if r_iter is not None:
        for rn in r_iter:
            yield rn
    for n in _neighbours(coord[:2]):
        if n == center:
            continue

        elif n[0] < 0:
            yield center[0] - 1, center[1], coord[2] - 1
        elif n[1] < 0:
            yield center[0], center[1] - 1, coord[2] - 1
        elif n[0] > maxs[0]:
            yield center[0] + 1, center[1], coord[2] - 1
        elif n[1] > maxs[1]:
            yield center[0], center[1] + 1, coord[2] - 1
        else:
            yield n + (coord[2],)


def make_map(s: [str]) -> Tuple[CellMap, Tuple[int, int]]:
    cell_map = set()
    max_x, max_y = 0, 0
    for y, line in enumerate(s):
        for x, cell in enumerate(line):
            max_x, max_y = max(max_x, x), max(max_y, y)
            if cell == '#':
                cell_map.add((x, y, 0))

    return cell_map, (max_x, max_y)


def automata_tick(cell_map: CellMap, maxs: Tuple[int, int]) -> CellMap:
    new_map = set()
    levels = set(chain.from_iterable(map(lambda x: (x[2] - 1, x[2], x[2] + 1), cell_map)))
    center = (maxs[0] // 2, maxs[1] // 2)
    for coord in product(range(maxs[0] + 1), range(maxs[1] + 1), iter(levels)):
        if coord in cell_map:
            if len(tuple(filter(lambda n: n in cell_map, neighbours(coord, maxs)))) == 1:
                new_map.add(coord)
        elif coord[:2] != center:
            if 1 <= len(tuple(filter(lambda n: n in cell_map, neighbours(coord, maxs)))) <= 2:
                new_map.add(coord)
    return new_map


def run_until_rep(initial_cell_map: CellMap, maxs: Tuple[int, int]) -> CellMap:
    visited = set()
    cell_map = initial_cell_map
    key = tuple(sorted(cell_map))
    while key not in visited:
        visited.add(key)
        print_cell_map(cell_map, maxs)
        cell_map = automata_tick(cell_map, maxs)
        key = tuple(sorted(cell_map))
    print_cell_map(cell_map, maxs)
    return cell_map


def run(initial_cell_map: CellMap, maxs: Tuple[int, int], times: int) -> CellMap:
    cell_map = initial_cell_map
    for _ in range(times):
        # print_cell_map(cell_map, maxs)
        cell_map = automata_tick(cell_map, maxs)
    print_cell_map(cell_map, maxs)
    return cell_map


def print_cell_map(cell_map: CellMap, maxs: Tuple[int, int]):
    s = ''
    levels = sorted(set(chain.from_iterable(map(lambda x: (x[2] - 1, x[2], x[2] + 1), cell_map))))
    for level in levels:
        s += 'Level {}\n'.format(level)
        for y in range(maxs[1] + 1):
            for x in range(maxs[0] + 1):
                if (x, y, level) in cell_map:
                    s += '#'
                elif (x, y) == (maxs[0] // 2, maxs[1] // 2):
                    s += '?'
                else:
                    s += '.'
            s += '\n'
        s += '\n'
    print(s[:-1])


if __name__ == '__main__':
    _initial_cell_map, _maxs = make_map(_data.splitlines())
    # _cell_map = run_until_rep(_initial_cell_map, _maxs)
    # _tot = 0
    # for (_x, _y) in _cell_map:
    #     _tot += 2 ** (_x + 5 * _y)
    # print(_tot)

    _cell_map = run(_initial_cell_map, _maxs, 200)
    print(len(_cell_map))
