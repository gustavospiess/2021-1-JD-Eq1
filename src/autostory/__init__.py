__version__ = "0.0.1"

from .map_generators import raw
from .text_generators import MapBuilder

from pprint import pp

def generate_json():
    raw_data = raw(size = 3, size_factor = 5)
    builder = MapBuilder()

    locked_edges = {k.door: k for k in raw_data.keys}

    for edge in raw_data.edges:
        origin = edge.origin.identifier
        destin = edge.destin.identifier

        builder.create_passage(origin, destin, locked_edges.get(edge))

    for vertex in raw_data.vertexes:
        builder.create_ambient(vertex.identifier)

    builder.first_ambient = raw_data.initial.identifier

    return builder.build().as_json()
