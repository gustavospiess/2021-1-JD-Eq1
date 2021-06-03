from typing import NamedTuple
from random import choice, randint, sample
import random


__doc___ = '''
This module is used to generate the graph of a game map.
The graph is divided in partition in such way that to any two partitions, there
are at most one edge between this two.

This partitions are linked in a tree structure, internally it can be any
ordinary graph, but between two partitions there are only one possible walk.

To every edge that link two partitions `a` and `b`, it is considered locked, the
key is granted to be in a partition bigger then min(a, b), this way, the
navigation starting from the last partition can go through every vertex.
'''


class Raw(NamedTuple):
    vertexes: set
    edges: set
    keys: set
    final: 'Vertex'


class Vertex(NamedTuple):
    area: int
    sub_area: int


class Edge(NamedTuple):
    origin: 'Vertex'
    destin: 'Vertex'


class Key(NamedTuple):
    position: 'Vertex'
    door: 'Edge'


def raw(size = 4, size_factor = 2):

    if not size:
        size = 4

    if not size_factor:
        size_factor = 1

    vertexes = [Vertex(i, 0) for i in range(size)]
    edges = []
    keys = []
    for i in range(0, size-1):
        e = Edge(vertexes[i], choice(vertexes[i+1:]))
        k = Key(vertexes[i+1], e)
        edges.append(e)
        keys.append(k)

    for room in vertexes[1:]:
        area = [room]
        minimum = size_factor//2
        maximum = size_factor*len(tuple(e for e in edges if room in e))
        for i in range(1, randint(minimum, maximum)):
            edge_count = randint(1, i)
            to_connect = sample(area, edge_count)
            new_room = Vertex(room.area, i)
            area.append(new_room)
            vertexes.append(new_room)
            for other in to_connect:
                edges.append(Edge(other, new_room))

        if room.area < len(keys):
            edges[room.area] = Edge(choice(area), edges[room.area].destin)
            try:
                keys[room.area-1] = Key(
                        choice(tuple(a for a in area if a not in edges[room.area])),
                        keys[room.area-1][1])
            except IndexError:
                keys[room.area-1] = Key(
                        area[0],
                        keys[room.area-1][1])

    return Raw(set(vertexes), set(edges), set(keys), vertexes[0])

