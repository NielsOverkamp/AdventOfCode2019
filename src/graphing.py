from collections import defaultdict
from heapq import heappop, heappush
from typing import TypeVar, Generic, Callable, Iterable, Tuple, Union, Dict

import math


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

    def _remove_connected(self, node: 'Graph[KT, VT]'):
        self.connected = filter(lambda c: c is not node, self.connected)

    def remove_connected(self, node: 'Graph[KT, VT]'):
        self._remove_connected(node)
        node._remove_connected(self)

    def __str__(self):
        return "G({})".format(self.val)

    def __repr__(self):
        return self.__str__()


S = TypeVar('S')


def find_path(start_node: S, is_final: Callable[[S], bool], get_neighbours: Callable[[S], Iterable[Tuple[S, int]]]) \
        -> (Union[S, None], Dict[S, int], Dict[S, S]):
    frontier = [(0, hash(start_node), start_node)]
    prev = dict()
    dists = defaultdict(lambda: math.inf)
    dists[start_node] = 0

    while len(frontier) > 0:
        _, _, node = heappop(frontier)

        if is_final(node):
            return node, dists, prev

        for neighbour, cost in get_neighbours(node):

            dist = dists[node] + cost
            if neighbour not in dists:
                heappush(frontier, (dist, hash(neighbour), neighbour))

            if dist < dists[neighbour]:
                dists[neighbour] = dist
                prev[neighbour] = node
    return None, dists, prev
