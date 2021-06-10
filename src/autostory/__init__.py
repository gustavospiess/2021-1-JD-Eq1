__version__ = "0.0.1"

from .map_generators import raw
from .text_generators import MapBuilder

from pprint import pp

def generate_json():
    raw_data = raw(size = 3, size_factor = 5)
    builder = MapBuilder()

    locked_edges = {k.door for k in raw_data.keys}

    for edge in raw_data.edges:
        origin = edge.origin.identifier
        destin = edge.destin.identifier

        is_locked = edge in locked_edges

        builder.create_passage(origin, destin, is_locked)

    for vertex in raw_data.vertexes:
        builder.create_ambient(vertex.identifier)

    return builder.build().as_json()
