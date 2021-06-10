from .. import map_generators
import collections


def test_raw_generation():
    _map = map_generators.raw(8, 5)
    assert isinstance(_map, map_generators.Raw)
    assert _map.vertexes.issuperset({map_generators.Vertex(i, 0) for i in range(8)})
    # contains at_least 8 areas numbered 0 to 7

    reached = {_map.final}
    stack = collections.deque([_map.final])

    while stack:
        v = stack.pop()
        for v1, v2 in _map.edges:
            if v1 == v and v2 not in reached:
                stack.append(v2)
            if v2 == v and v1 not in reached:
                stack.append(v1)
        reached.add(v)

    assert len(reached) == len(_map.vertexes)

    assert len(_map.keys) == 7
    # there are exacly n-1 keys

    for room, door in _map.keys:
        assert room.area > min(door, key=lambda r: r.area).area
        # every key can be found in a room not locked by it

    count_area_change = len(tuple(d for d in _map.edges if d[0].area != d[1].area))
    assert count_area_change == 7
    # assert there are exacly 7 edges that link different areas

    assert len(_map.vertexes) <= 5*8*2
    assert len(_map.vertexes) >= 1.2*8
    # assert that there are up to size_factor * size * 2 rooms

    assert len(map_generators.raw(0, 1).vertexes) >= 4 #assert minum size
    assert len(map_generators.raw().vertexes) >= 4
    assert len(map_generators.raw(size_factor=0).vertexes) >= 4


    assert len(tuple(k for k in _map.keys if k[0] in k[1])) <= 2
    # assert that the key is not in the room where its door is most of the time


def test_key_shuffle():
    count = 0
    for i in range(100):
        _map = map_generators.raw()
        count += len(tuple(k for k in _map.keys if k[0] in k[1]))
    assert count == 0
    # assert that the key is not in the room where its door is most of the time
