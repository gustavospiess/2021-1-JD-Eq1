from tracery import Grammar

from random import choice, sample
from abc import ABC, abstractproperty

from typing import Mapping, Union, Dict, List, Callable, Any, Tuple
from typing import Set, Iterable

from functools import partial, lru_cache
from itertools import chain
from collections import defaultdict

from dataclass_abc import dataclass_abc
from dataclasses import field, dataclass

from .. import datamodels

from .native_values import (
        _INTRO_LETTER,
        _LOCATION_NAMES,
        _MAP_BASE_DESCRIPTION,
        _MONSTER_NAME,
        _PASSAGE_BASE_DESCRIPTION,
        _PLACE_BASE_DESCRIPTION,
        )

from .word_types import (
        Substantive,
        Adjective,
        )

from .generation_base_data import (
        _PlaceType,
        _Flavor,
        _PassageType,
        _MapType,
        _MAP_TYPE,
        _MAP_FLAVOR_LIST,
        _PLACE_FLAVOR_LIST,
        _SECONDATY_PLACE_FLAVOR_LIST,
        )


def monster_names() -> str:
    g = Grammar(_MONSTER_NAME)
    while True:
        yield g.flatten('#main#')


def intro_letter() -> str:
    g = Grammar(_INTRO_LETTER)
    while True:
        yield g.flatten('#main#')


def location_names() -> str:
    g = Grammar(_LOCATION_NAMES)
    while True:
        yield g.flatten('#main#')


RAW_GRAMMAR_TYPE = Dict[str, Union[str, List[str]]]

@dataclass_abc
class GrammerMakebla(ABC):
    __frozen: bool = field(init=False, default=False)

    def freeze(self):
        self.__frozen = True
        descritption = self.describe()
        self.describe = lambda: descritption

    @abstractproperty
    def context(self) -> 'Context':
        pass

    @abstractproperty
    def base_description(self) -> str:
        pass

    @abstractproperty
    def raw_grammar(self) -> RAW_GRAMMAR_TYPE:
        pass

    @property
    @lru_cache
    def grammar(self) -> Grammar:
        g = Grammar(self.raw_grammar)
        g.add_modifiers(self.context.make_modifires(g))
        return g

    
    def describe(self) -> str:
        desc = self.grammar.flatten(self.base_description)
        return desc.replace('\n', ' ').replace('  ', ' ').replace(' .', '.').strip()


@dataclass_abc(unsafe_hash=True)
class Map(GrammerMakebla):
    context: 'Context' = field(compare=False)
    base_type: '_MapType'
    flavor: '_Flavor'
    name: str

    @property
    def base_description(self) -> str:
        return _MAP_BASE_DESCRIPTION

    _LOCATION_NAMES_GENERATOR = location_names()

    @classmethod
    def _composed_map_flavor(cls):
        return _Flavor.join(*sample(_MAP_FLAVOR_LIST, 3))

    @classmethod
    def make(cls, context):
        base_type: '_MapType' = _MAP_TYPE
        flavor: '_Flavor' = cls._composed_map_flavor()
        name: str = next(cls._LOCATION_NAMES_GENERATOR)

        return cls(
                context = context,
                base_type=base_type,
                flavor=flavor,
                name=name)

    @property
    @lru_cache
    def raw_grammar(self):
        return {
                'empty': '',
                'nome': self.name,
                **self.flavor.raw(context=self.context),
                **self.base_type.raw('tipo', context=self.context)
                }


@dataclass_abc(unsafe_hash=True)
class DecorationItem(GrammerMakebla):
    decoration_type: '_DecorationItemType'
    context: 'Context' = field(compare=False)

    @property
    def base_description(self) -> str:
        return '#main#'

    @property
    @lru_cache
    def desc(self):
        return self.decoration_type.desc

    @property
    @lru_cache
    def raw_grammar(self):
        deco = self.decoration_type
        return {
                'empty': '',
                **deco.desc.raw('nome', context=self.context),
                **choice(deco.flavor_list).raw(context=self.context),
                'main': '#nome_um# #nome##_adjetivo#',
                '_adjetivo': '[adj:adjetivo_#nome_o#]#_sub_adj#',
                '_sub_adj': ['', ' #empty.norepeat(adj)#', ' #empty.norepeat(adj)#']
                }


@dataclass_abc(unsafe_hash=True)
class Place(GrammerMakebla):
    context: 'Context' = field(compare=False)
    place_type: _PlaceType
    flavor_sec: _Flavor
    flavor_ter: _Flavor
    decorations: Tuple['DecorationItem']
    passages: Tuple['Passage']

    @property
    def base_description(self) -> str:
        return '#desc##decorations#'

    @classmethod
    def make(cls, place_type: _PlaceType, context: 'Context', passages) -> 'Place':
        flavor_sec = choice(_PLACE_FLAVOR_LIST)
        flavor_ter = choice(_SECONDATY_PLACE_FLAVOR_LIST)

        decorations = tuple(DecorationItem(deco, context) for deco in map(choice, place_type.decorations) if deco is not None)

        return cls(
                context = context,
                place_type = place_type,
                flavor_sec = flavor_sec,
                flavor_ter = flavor_ter,
                decorations = decorations,
                passages = passages
                )

    @property
    @lru_cache
    def nome(self) -> Substantive:
        return self.place_type.desc

    @property
    def raw_grammar(self):
        _raw_grammar = {'empty': ''}
        _raw_grammar['desc'] = _PLACE_BASE_DESCRIPTION

        decor_desc_tuple = tuple(d.describe() for d in chain(self.decorations, self.passages))
        listed_decoration = None
        if (len(decor_desc_tuple) > 1):
            decor_desc_tuple = tuple(sorted(decor_desc_tuple, key=len))
            listed_decoration = ', '.join(decor_desc_tuple[:-1]) + f' e {decor_desc_tuple[-1]}'
        elif decor_desc_tuple:
            listed_decoration = decor_desc_tuple[0]

        if (listed_decoration):
            _raw_grammar['decorations'] = ' onde você pode ver ' + listed_decoration
        else:
            _raw_grammar['decorations'] = ''

        _raw_grammar.update(self.nome.raw('tipo'))
        _raw_grammar.update(self.flavor_sec.raw('adjetivo'))
        _raw_grammar.update(self.flavor_ter.raw('adjetivo_comp'))
        return _raw_grammar


@dataclass_abc(unsafe_hash=True)
class Key(GrammerMakebla):
    context: 'Context' = field(compare=False)
    desc: Substantive
    flavor: _Flavor

    @classmethod
    def make(cls, passage_type: _PassageType, context: 'Context'):
        flavor = choice(passage_type.key_type.flavor_list)
        desc = passage_type.key_type.desc
        return Key(context, desc, flavor)

    @property
    def base_description(self):
        return '#desc# #adjetivo#'

    @property
    def raw_grammar(self):
        _raw_grammar = {'empty': ''}
        print(self.desc)
        _raw_grammar.update(self.desc.raw('desc'))
        _raw_grammar.update(self.flavor.raw('adjetivo'))
        return _raw_grammar


@dataclass_abc(unsafe_hash=True)
class Passage(GrammerMakebla):
    context: 'Context' = field(compare=False)
    nome: Substantive
    passage_type: _PassageType
    flavor: _Flavor

    @property
    def base_description(self) -> str:
        return '#desc#'

    @classmethod
    def make(cls, passage_type: _PassageType, context: 'Context') -> Tuple['Passage', 'Passage']:
        flavor = choice(passage_type.flavor_list)
        return (cls(context = context,
                    nome = passage_type.a_side,
                    flavor = flavor,
                    passage_type = passage_type,
                    ),
                cls(context = context, 
                    nome = passage_type.b_side,
                    flavor = flavor,
                    passage_type = passage_type,
                    ))

    @property
    def raw_grammar(self):
        _raw_grammar = {'empty': ''}
        _raw_grammar['desc'] = _PASSAGE_BASE_DESCRIPTION
        _raw_grammar.update(self.nome.raw('nome'))
        _raw_grammar.update(self.flavor.raw('adjetivo'))
        return _raw_grammar


class Context():
    class ContextualModifiers(Mapping['str', Callable[[str, Any], str]]):

        def __init__(self, grammar, context):
            self.grammar = grammar
            self.context = context
            self.__mapping = {
                'norepeat': partial(self.norepeat),
                'gender': partial(self.gender)
            }

        def gender(self, gender, text) -> str: 
            return self.grammar.flatten(f'#{text}_{gender}#')

        def norepeat(self, text=None, group=None) -> str:
            symbols = self.grammar.symbols

            if group not in symbols or not isinstance(symbols[group].raw_rules, list):
                return text
            
            options = symbols[group].raw_rules
            if len(options) == 1 and options[0] in symbols and options[0] != group: 
                # Sometimes the text to be not repeated is nested to treat gender
                # I know it is not pretty but I am neither and I'm not complaining
                return self.norepeat(text, options[0])
            return self.context.norepeat(options)


        def reset_norepeat(self) -> None:
            self.context._reset_norepeat_said()

        def __getitem__(self, key: str) -> Callable[[str, Any], str]:
            return self.__mapping[key]

        def __iter__(self):
            return iter(self.__mapping)

        def __len__(self):
            return len(self.__mapping)


    def __init__(self):
        self.map = Map.make(self)
        self.place_type_set: Set['_PlaceType'] = set()
        self._norepeat_said = set()
        self._norepeat_map = list()

    def make_modifires(self, grammar: Grammar):
        return self.ContextualModifiers(grammar, self)

    def norepeat(self, options):
        option_set = set(options)
        if option_set <= self._norepeat_said:
            self._reset_norepeat_said(option_set)
        text = choice(tuple(set(options) - self._norepeat_said))
        self._update_norepeat_said(text)
        return text

    def _update_norepeat_said(self, text):
        for group in self._norepeat_map:
            if text in group:
                self._norepeat_said |= group;
                break
        else:
            self._norepeat_map.append({text})
            self._norepeat_said |= {text}

    def _register_norepeat_map(self, options):
        for group in self._norepeat_map:
            if any(op in group for op in options):
                group |= options
                break
        else:
            self._norepeat_map.append(options)

    def _reset_norepeat_said(self, option_set=None):
        if option_set is None:
            self._norepeat_said = set()
            return
        self._norepeat_said -= option_set

    @property
    def map_type(self) -> _MapType:
        return self.map.base_type

    def __choose_place_type(self) -> '_PlaceType':
        can_repeat_func = lambda t: t.repeat or not t in self.place_type_set
        possible_place_type_tuple = tuple(filter(can_repeat_func, self.map_type.place_types))
        place_type = choice(possible_place_type_tuple) 
        return place_type

    def make_place(self, passages=tuple()) -> Place:
        place_type = self.__choose_place_type()
        place = Place.make(place_type, self, passages)

        self.place_type_set.add(place.place_type)
        return place
    

class MapBuilder():

    class __PassageMap(defaultdict):
        def __init__(self, *args, **kwargs):
            super().__init__(dict, *args, **kwargs)

        def iter_pairs(self):
            for _from, sub_dict in self.items():
                for _to, instace in sub_dict.items():
                    if _from > _to:
                        yield ((_to, instace,), (_from, self[_to][_from],))

    def __init__(self):
        self.context = Context()
        self.passage_map = self.__PassageMap()
        self.ambient_map = dict()
        self.key_map = dict()

    @property
    def ambient_list(self):
        return list(self.ambient_map.values())

    def create_passage(self, _from, _to, locked):
        types_available: Iterable[_PassageType] = self.context.map_type.passage_types
        if (locked):
            types_available = tuple(t for t in types_available if t.key_type)
        else:
            types_available = tuple(t for t in types_available if not t.key_type)

        passage_type = choice(types_available)
        a_side, b_side = Passage.make(passage_type, self.context)

        self.passage_map[_from][_to] = a_side
        self.passage_map[_to][_from] = b_side

        if locked:
            self.key_map[(_from, _to)] = Key.make(passage_type, self.context)

    def create_ambient(self, _id):
        passages = tuple(self.passage_map[_id].values())
        ambient = self.context.make_place(passages)
        self.ambient_map[_id] = ambient

    def build(self) -> datamodels.Map:

        for (f_id, f_inst), (t_id, t_inst) in self.passage_map.iter_pairs():
            f_inst.freeze()
            t_inst.freeze()

        for ambient in self.ambient_map.values():
            ambient.freeze()

        passage_list = list()
        for (f_id, f_inst), (t_id, t_inst) in self.passage_map.iter_pairs():
            passage_pair = (
                    datamodels.Passage(f_id, f_inst.describe()),
                    datamodels.Passage(t_id, t_inst.describe()))
            passage_list.append(passage_pair)

        ambient_list = list()
        for _id, _inst in self.ambient_map.items():
            decoration_list = list()
            for deco in _inst.decorations:
                decoration_list.append(deco.describe())

            sub_passage_list = list()
            for passage in _inst.passages:
                sub_passage_list.append(passage.describe())

            ambient = datamodels.Ambient(
                    id=_id,
                    descritption = _inst.describe(),
                    passages = tuple(sub_passage_list),
                    decorations = tuple(decoration_list),
                    )
            ambient_list.append(ambient)

        keys = list()
        for (_from, _to), inst in self.key_map.items():
            keys.append(datamodels.Key(
                _to,
                0, #TODO
                inst.describe(),
                ))

        
        return datamodels.Map(
                    introducion_letter = next(intro_letter()),
                    name = self.context.map.name,
                    descritption = self.context.map.describe(),
                    ambients = tuple(ambient_list),
                    passages = tuple(passage_list),
                    keys = tuple(keys)
                )

