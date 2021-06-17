from typing import NamedTuple
from random import choice, randint, shuffle


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
    initial: 'Vertex'
    final: 'Vertex'


class Vertex(NamedTuple):
    area: int
    sub_area: int

    @property
    def identifier(self) -> str:
        return f'{self.area}_{self.sub_area}'


class Edge(NamedTuple):
    origin: 'Vertex'
    destin: 'Vertex'


class Key(NamedTuple):
    position: 'Vertex'
    door: 'Edge'


def raw(size = 3, size_factor = 4) -> Raw:
    if not size or size < 3:
        size = 3
    if not size_factor or size_factor < 4:
        size_factor = 4

    vertexes = [Vertex(0, 0)]
    edges = []
    keys = []

    for area_id in range(1, size):
        vertexes.append(Vertex(area_id, 0))
        minimum_sub_size = size_factor//2+1
        maximum_sub_size = size_factor*2-1
        sub_size = randint(minimum_sub_size, maximum_sub_size)
        for sub_area_id in range(1, sub_size):
            new_vertex = Vertex(area_id, sub_area_id)
            minimum_connection = 1
            maximum_connection = min(sub_area_id, 3)
            connection_amount = randint(minimum_connection, maximum_connection)
            for connection_id in range(connection_amount):
                edges.append(Edge(
                    new_vertex,
                    choice(tuple(v for v in vertexes if v.area == area_id))
                    ))
            vertexes.append(new_vertex)

    for area_id in range(0, size-1):
        previous = [area_id + 1, randint(min(area_id+1, size-1), size-1)]
        shuffle(previous)
        key_area, door_area = previous

        new_edge = Edge(
                choice(tuple(v for v in vertexes if v.area == door_area)),
                choice(tuple(v for v in vertexes if v.area == area_id)),
                )
        new_key = Key(
                choice(tuple(v for v in vertexes if v.area == key_area and v not in new_edge)),
                new_edge,
                )
        edges.append(new_edge)
        keys.append(new_key)


    return Raw(
        vertexes = set(vertexes),
        edges = set(edges),
        keys = set(keys),
        initial = vertexes[-1],
        final = vertexes[0]) 
