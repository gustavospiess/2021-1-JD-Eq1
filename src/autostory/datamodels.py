from typing import NamedTuple
from typing import Mapping, Tuple

import json


class Decoration(NamedTuple):
    descritption: str


class Passage(NamedTuple):
    destination: str
    origin: str
    descritption: str


class Key(NamedTuple):
    destination: str
    place: str
    descritption: str


class Ambient(NamedTuple):
    id: str
    descritption: str
    passages: Tuple[Passage, ...]
    decorations: Tuple[Decoration, ...]


class Map(NamedTuple):
    introducion_letter: str
    name: str
    descritption: str
    first_ambient: str
    ambients: Tuple[Ambient, ...]
    passages: Tuple[Passage, ...]
    keys: Tuple[Key]

    def as_dict(self):
        return {
                    'introducion_letter': self.introducion_letter,
                    'name': self.name,
                    'descritption': self.descritption,
                    'first_ambient': self.first_ambient,
                    'ambients': tuple(a._asdict() for a in self.ambients),
                    'passages': tuple(p._asdict() for p in self.passages),
                    'keys': tuple(k._asdict() for k in self.keys)
                }

    def as_json(self):
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=2)
