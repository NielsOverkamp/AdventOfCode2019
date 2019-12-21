from collections import deque, defaultdict
from enum import Enum
from heapq import heappop, heappush
from typing import TypeVar, Generic, Callable, Iterable, Tuple, Union, Dict

import math
from itertools import repeat

from print_2d import String2DBuilder

_data = '''#################################################################################
#...#...............#...........#.......#.#...........#..z......#...K........r..#
###.#.#############.#.#.#######.#.###.#.#.#.#####.###.###.#######.#.#############
#...#.#.....#...#...#.#.#.......#...#.#.#.#.....#.#.....C.#.......#.#.....#.....#
#.###.#.###.#.#.#.###.#.###########.#.###.#####.#.#####.###.#######.#.###.#.###.#
#...#.#.#.#b#.#...#...#...........#.#...#.....#.#.....#.#...#.....#.....#...#...#
###.#.#.#.#.#.#####.###########.###.###.#T#####.#####.###.###P###.#########.#.#R#
#...#.#...#.#f....#.....#...#...#...#.#.#.#...#.Y.#...#.....#.#.#..p#a....#.#.#.#
#.#.#.#####.#####.#####.#.#.#.###.###.#.#.#.#.###.#.###.#####.#.###.#.###.#.#.#.#
#.#.#.....#.#.....#...#...#.#.....#...#.#.#.#.#...#.....#.....#...#.#.#.#.#.#.#.#
#.#######.#.#.#######.#####.#######.###.#.#.#.#.#########.#######.#.#.#G#.###.#.#
#..q#.......#.......#.....#.#.......#.U.#.#.#...#....n..#v..#.L...#.#.#.....#.#.#
#.#.#.#######.#####.#.###.#.#.#####.#.#.#.#.###########.###.###.#.#.#.#####.#.#.#
#.#...#.....#...#...#.#...#.#.#.....#.#.#...#...........#.#...#.#.#.#.....#...#.#
#.#####.###.#####.#####.#.#.#.#.#####.#.#.#####.#.#####.#.###.#.###.#.###.#####.#
#.....#.#...#.....#.....#.#...#...#...#.#.#...#.#...#.#.#.#...#.#...#.#.#...#..g#
###X###.#.###.#####.#############.#.###.#.#.#.#####.#.#.#.#.###.#.###.#.###.#####
#...#...#.....#...#...........D...#.#.#.#...#.#.....#...#.#.#.....#...A...#.....#
#.###.#########.#.#.###########.###.#.#.#####.#.#####.###.#.###.#########.#####.#
#...#.#.....#...#.....#...#...#.#...#...#.....#.#...#.#...#...#l#...#.#j..#...#.#
#.###.#.#####.#########.#.#.#.#.#.#####.#.#####.###.#.###.###V#.#.#.#.#.###.#J#.#
#.#...#.....#.#.....#...#...#.#.#...S.#.#...#.....#.#.....#.#.#...#.#.....#.#...#
#.#.###.###.#.#.###.#########.#.#####.#.###.#####.#.#####.#.#######H#######.#####
#.#...#...#.#.#...#...#...#...#.....#.#.#...#.....#.....#.#...#...#........h#...#
#.###I###.#.#.#.###.#.#.#.#.#########.###.###.#######.#.#.#.#.#.#.#############B#
#...#...#.#.#.#.#...#.#.#.#.#.......#...#.....#.......#.#.#.#...#...#...#.......#
###.###.#.#M#.#.#.###.###.#.#.#####.###.#######.#######.#.#.#######.#.#.###.###.#
#.#.#.#.#.#...#.#...#.....#...#.#...#...#...#.....#...#.#...#.....#...#.....#.#.#
#.#.#.#.#.#####.###.###########.#.###.###.#.#.###.###.#.#####.#.#############.#.#
#.#...#.#.....#.#.#...#...........#.#...#.#.#...#.#...#.#...#.#...............#.#
#.###.#.#####.#.#.###.#.###########.#.#.#.#.###.#.#.###.#.###.#########.#####.#.#
#...#.#.#.#...#.#...#.#.#.....#...#...#.#.#...#.#.#.....#.#...#.....#.#...#...#.#
###.#.#.#.#.###.#.###.#.#.###.###.#.###.#####.#.#.#.#####.#.#####.#.#.###.#####.#
#...#.#.#...#...#...#...#.#.#...#.....#.#.....#.#.#.......#.......#.#...#.......#
#.#O#.#.#####.#####.#####.#.###.#.#####.#.###.#.#.#################.###.#########
#.#.#.#...#...#...........#.....#.#...#.#.#...#.#...#.......#.......#.....#.....#
#.#.#.###.#.###.###########.#######.#.#.#.###.#.###.#.###.###.#######.###.###.#.#
#.#.#.#.#...#...#.#.......#...#.....#.#.#...#.#...#.#.#.#.#...#.........#.#...#.#
#.###.#.#######.#.#.#.#######.#.#####.#.#.#.#####.#.#.#.#.#.###########.#.#.###.#
#.........E.....#...#...........#.........#.......#....e#...............#...#...#
#######################################.@.#######################################
#.....#...#.........#...............#.........#...#.............#...#...#...#...#
#.###.#.#.#######.#.###.###########.###.#.#####.#.#.#.#########.#.#.#.#.#.#.###.#
#.#.#...#.....#...#...#...#.....#.#.#...#.......#...#.....#.#...#.#...#.#.#.....#
#.#.#########.#.#####.#.#.#.###.#.#.#.###.###############.#.#.###.#####.#.#####.#
#.#.#...#...#...#.#...#.#.#...#...#.#...#.#.......#...#...#.#.....#.#...#.#x#...#
#.#.#.#.#.#.#####.#.#####.#.#.###.#.###.#.#####.#.#.#.#.###.#######.#.###.#.#.###
#.#...#...#.#...#...#.....#.#...#.#.....#...#...#.#.#.#...#.........#....o#...#.#
#.#####.###.#.#.#.###.#####.###.#######.###.#.###.#.#####.###.#############.###.#
#.#...#.#.#.#.#...#.#.....#.#...#.....#s#...#.#.#.#.....#...#...........#.#.....#
#.#.#.#.#.#.#.#####.#.###.#.#.#.#.###.#.#.###.#.#.###.#.###.#########.#.#.#####.#
#...#.#.#.#...#...#...#...#.#.#.#...#.#.#.....#.......#.#.#.#.........#.......#.#
#.###.#.#.#####.#.#####.#####.#.###.#.#.###.###########.#.#.#.#########.#######.#
#.#.#.#.#.......#.......#.....#.#...#...#...#...#.....#...#.#.#..m......#.....#.#
#.#.#.#.###.#############.#######.#######.###.#.#.###.#.###.#.#.#####.###.###.#.#
#...#.#...#.....#.....#.....#...#.#.....#...#.#.#...#...#...#.#.#...#...#...#...#
###.#.###.#.###.#####.#.###.#.#.#.#.###.#.###.#.#########.###.###.#.#######.#####
#...#.#.#.#...#.....#.#.#.#...#...#...#.#.#...#.......#...#.......#.......#.Q...#
#.###.#.#.#.#######.#.#.#.#############.#.#.#########.#.#########.#######.#####.#
#...#.#...#.#.......#.......#...........#.#.#.......#...#.......#.......#...#...#
###.#.#.###.#.#####.#######.#.#.#######.#.#.#.#####.#####.#.###.#######.###.#.###
#...#.#.#.#.#.#.....#.#...#.#.#.......#.#.#.#.....#.#...#.#.#.#.#.....#...#...#.#
#####.#.#.#.#.###.###.#.#.#.#.#######.###.#.#.#####.#.#.#.###.#.#.#.#.###.#####.#
#...W.#.#...#...#.#...#.#.#.#.......#...#u#...#.....#.#.#.....#.#.#.#.#.#.#.....#
#.#####.###.###.###.#####.#.#######.###.#######.###.#.#.#######.###.#.#.#.#.#####
#.#...#...#.#.#.#...#.....#.#.........#.#...#...#...#.#...#...#.#...#...#.#w....#
#.#.#.###.#.#.#.#.###.#.###.#.#########.#.#.#.#.#####.###.#.#.#.#.#######.###.#.#
#.#.#.#.#.#...#.#.#...#.#...#...#.#.....#.#...#.#...#.#.#...#...#...#...#...#.#.#
#.#.#.#.#.#####.#.#.#####.#####.#.#.###.#.#######.#.#.#.#########.#.#.#.###.###.#
#.#.#.#.........#.#.....#.#...#...#.#...#.#.....#.#.#.....#.....#.#...#...#...#.#
#.#.#.###.#######.#####.#.#.#.###.#.###.#.#.###.#.#.#####.#####.#.#######.###F#.#
#t..#...#.#.......#.....#...#.#...#...#.#.#.#.#.#.#.....#.#.....#...#...#.#...#.#
#.#####.###.#######.#########.#######.#.#.#.#.#.#.###.#.#.#.#######.#N#.#.#.###.#
#.....#...#.#...............#.#.......#.#.#.#.#...#.#.#.#.#.......#...#.#...#...#
#########.#.#####.#####.###.#.#.#######.#.#.#.#####.#.###.#.#####.#####.#####.#.#
#........y#.....#.#...#.#...#.#.#.......#...#.......#.....#.#.....#...#....i..#.#
#.#############.#.#.#.#.###.#.#.#.###########.###.#########.#.#####.#.#########.#
#...#.......#...#.#.#.#...#.#.#.#.#.....#..k#...#.....#c..#.#.....#.#...#.....#.#
#.#.#.#####.#.###.#.#.###.###.#.#.###.#.#.#####.#####.#.#.#.#####.#.###.#.###.#.#
#.#.......#...#.....#...#.......#..d..#.#.......Z...#...#.......#.....#.....#...#
#################################################################################'''


# _data = '''#################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################'''


# _data = '''#########
# #b.A.@.a#
# #########'''

# _data = '''#######
# #a.#Cd#
# ##...##
# ##.@.##
# ##...##
# #cB#Ab#
# #######'''
#
# _data = '''#############
# #DcBa.#.GhKl#
# #.###...#I###
# #e#d#.@.#j#k#
# ###C#...###J#
# #fEbA.#.FgHi#
# #############'''
#
# _data = '''#############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba...BcIJ#
# #####.@.#####
# #nK.L...G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############'''

class Tile:
    passable: bool
    char: str

    def __init__(self, char, passable):
        self.passable = passable
        self.char = char

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.__str__()


wall = Tile('#', False)
corridor = Tile(' ', True)


class Key(Tile):
    def __init__(self, char):
        super().__init__(char, passable=True)


class Door(Tile):
    def __init__(self, char):
        super().__init__(char, passable=True)


def neighbours(pos, maxs=(math.inf, math.inf)):
    return iter(filter(lambda x: 0 <= x[0] <= maxs[0] and 0 <= x[1] <= maxs[1],
                       map(lambda x: (pos[0] + x[0], pos[1] + x[1]), ((0, 1), (1, 0), (0, -1), (-1, 0)))))


VT = TypeVar('VT')
KT = TypeVar('KT')


class Graph(Generic[VT]):
    val: VT
    connected: [('Graph[KT, VT]', int)]

    def __init__(self, val):
        self.val = val
        self.connected = []

    def _add_connected(self, node: 'Graph[KT, VT]', cost: int):
        self.connected.append((node, cost))

    def add_connected(self, node: 'Graph[KT, VT]', cost: int):
        self._add_connected(node, cost)
        node._add_connected(self, cost)

    def add_connected_if_smallest(self, node: 'Graph[KT, VT]', cost: int):
        unique = True
        for cnode, ccost in self.connected:
            if cnode == node:
                unique = False
                if ccost > cost:
                    self.remove_connected(cnode)
                    self.add_connected(node, cost)
                    return
        if unique:
            self.add_connected(node, cost)

    def _remove_connected(self, node: 'Graph[KT, VT]'):
        self.connected = filter(lambda c: c is not node, self.connected)

    def remove_connected(self, node: 'Graph[KT, VT]'):
        self._remove_connected(node)
        node._remove_connected(self)

    def __str__(self):
        return "G({})".format(self.val)

    def __repr__(self):
        return self.__str__()


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def sorted_str(s: str):
    return ''.join(sorted(s))


def make_map(maze_lists):
    maze_map: {(int, int): Tile} = dict()
    pos: (int, int) = (math.inf, math.inf)

    for y, line in enumerate(maze_lists):
        for x, cell in enumerate(line):
            if cell == '@':
                maze_map[(x, y)] = corridor
                pos = (x, y)
            elif cell == '#':
                maze_map[(x, y)] = wall
            elif cell == '.':
                maze_map[(x, y)] = corridor
            elif 'a' <= cell <= 'z':
                maze_map[(x, y)] = Key(cell)
            elif 'A' <= cell <= 'Z':
                maze_map[(x, y)] = Door(cell)
            else:
                raise Exception("Unknown cell {}".format(cell))

    return maze_map, pos


def make_graph(maze_map, pos):
    maxs = max(maze_map)
    maze_root: Graph[Tile] = Graph(corridor)
    frontier = deque(list(
        zip(filter(lambda x: maze_map[x] != wall, neighbours(pos, maxs)),
            repeat(maze_root), repeat(1), repeat(pos))))
    pos_node_map = {pos: maze_root}
    visited = {pos}
    for cell, _, _, _ in frontier:
        visited.add(cell)
    while len(frontier) > 0:
        cell, node, cost, tail = frontier.pop()
        ns = list(filter(lambda x: maze_map[x] != wall, neighbours(cell, maxs)))
        if len(ns) != 2 or maze_map[cell] != corridor:
            # We make a node!
            extending_node = node
            node = Graph(maze_map[cell])
            node.add_connected(extending_node, cost)
            pos_node_map[cell] = node
            cost = 0
        if len(ns) == 1:
            continue

        for n in ns:
            if n != tail and n in pos_node_map:
                node.add_connected(pos_node_map[n], cost + 1)
            if n not in visited:
                frontier.append((n, node, cost + 1, cell))
                visited.add(n)
    return maze_root


def compress_graph(maze_graph: Graph[Tile]):
    # def get_neighbours(node: Graph[Tile]):
    #     pass

    frontier = deque([maze_graph])
    visited = {maze_graph}
    old_to_new = {maze_graph: Graph(corridor)}
    while len(frontier) > 0:
        dists: Dict[Graph[Tile], int]
        prev: Dict[Graph[Tile], Graph[Tile]]
        start = frontier.popleft()
        visited.add(start)
        new_start = old_to_new[start]
        (_, dists, prev) = find_path(start, lambda x: False, lambda x: x.connected)
        for node in dists.keys():
            if node.val != corridor and node not in visited:
                prev_node = prev[node]
                while prev_node.val == corridor and prev_node != start:
                    prev_node = prev[prev_node]
                if prev_node == start:
                    if node not in old_to_new:
                        neighbour = Graph(node.val)
                        old_to_new[node] = neighbour
                    else:
                        neighbour = old_to_new[node]
                    new_start.add_connected_if_smallest(neighbour, dists[node])
                    frontier.append(node)
    return old_to_new[maze_graph]


S = TypeVar('S')


def find_path(start_node: S, is_final: Callable[[S], bool], get_neighbours: Callable[[S], Iterable[Tuple[S, int]]], heuristic: Callable[[S], int] = None) \
        -> (Union[S, None], Dict[S, int], Dict[S, S]):

    def _heuristic(node: S):
        if heuristic is None:
            return 0
        else:
            return heuristic(node)

    frontier = [(0 + _heuristic(start_node), hash(start_node), start_node)]
    prev = dict()
    dists = defaultdict(lambda: math.inf)
    dists[start_node] = 0

    while len(frontier) > 0:
        c, _, node = heappop(frontier)
        if is_final(node):
            return node, dists, prev

        for neighbour, cost in get_neighbours(node):

            dist = dists[node] + cost
            if neighbour not in dists:
                heappush(frontier, (dist + _heuristic(node), hash(neighbour), neighbour))

            if dist < dists[neighbour]:
                dists[neighbour] = dist
                prev[neighbour] = node
    return None, dists, prev


def run():
    print(_data)
    maze_lists: [str] = _data.splitlines()

    maze_map, pos = make_map(maze_lists)

    maze_root = make_graph(maze_map, pos)

    final_keys = ''.join(sorted(map(lambda x: x.char, filter(lambda x: type(x) == Key, maze_map.values()))))

    max_num_keys = 0

    def is_final(node):
        nonlocal max_num_keys
        if len(node[1]) > max_num_keys:
            max_num_keys = len(node[1])
            print(max_num_keys)
        return node[1] == final_keys

    def get_neighbours(node):
        graph_node, keys = node
        for neighbour, cost in graph_node.connected:
            if type(neighbour.val) == Key and neighbour.val.char not in keys:
                neighbour_keys = sorted_str(keys + neighbour.val.char)
            elif type(neighbour.val) == Door and neighbour.val.char.lower() not in keys:
                continue
            elif type(neighbour.val) == Door:
                neighbour_keys = keys
            else:
                neighbour_keys = keys
            yield (neighbour, neighbour_keys), cost

    # final_state, dists, prev = find_path((maze_root, ''), is_final, get_neighbours)
    #
    # print((final_state, dists[final_state]))

    new_maze_map = maze_map.copy()
    new_maze_map[pos] = wall
    for n in neighbours(pos):
        new_maze_map[n] = wall

    str_maze = String2DBuilder(map(lambda x: (x[0], str(x[1])), new_maze_map.items()))
    str_maze.print()

    poss = ((pos[0] + 1, pos[1] + 1), (pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1] + 1), (pos[0] - 1, pos[1] - 1))
    maze_roots = tuple(map(lambda pos: compress_graph(make_graph(new_maze_map, pos)), poss))

    def new_get_neighbours(node: ((Graph[Tile], Graph[Tile], Graph[Tile], Graph[Tile]), str)):
        graph_nodes, keys = node
        for i in range(len(graph_nodes)):
            for (graph_neighbour, keys_neighbour), cost in get_neighbours((graph_nodes[i], keys)):
                yield (graph_nodes[:i] + (graph_neighbour,) + graph_nodes[i + 1:], keys_neighbour), cost

    def heuristic(node: ((Graph[Tile], Graph[Tile], Graph[Tile], Graph[Tile]), str)):
        return (len(final_keys) - len(node[1])) * 20

    final_state, dists, prev = find_path((maze_roots, ''), is_final, new_get_neighbours, heuristic)
    print((final_state, dists[final_state]))


if __name__ == '__main__':
    run()
