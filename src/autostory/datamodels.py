from typing import NamedTuple
from typing import Mapping, Tuple

import json


class Decoration(NamedTuple):
    descritption: str


class Passage(NamedTuple):
    destination: int
    descritption: str


class Key(NamedTuple):
    destination: int
    place: int
    descritption: str


class Ambient(NamedTuple):
    id: int
    descritption: str
    passages: Tuple[Passage, ...]
    decorations: Tuple[Decoration, ...]


class Map(NamedTuple):
    introducion_letter: str
    name: str
    descritption: str
    ambients: Tuple[Ambient, ...]
    passages: Tuple[Tuple[Passage, Passage], ...]
    keys: Tuple[Key]

    def as_dict(self):
        return {
                    'introducion_letter': self.introducion_letter,
                    'name': self.name,
                    'descritption': self.descritption,
                    'ambients': tuple(a._asdict() for a in self.ambients),
                    'passages': tuple((p1._asdict(), p2._asdict(),) for p1, p2 in self.passages),
                    'keys': tuple(k._asdict() for k in self.keys)
                }

    def as_json(self):
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=2)
