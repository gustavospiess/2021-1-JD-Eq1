import tracery
from collections.abc import Mapping
from random import choice, sample
from functools import partial, lru_cache
from dataclasses import dataclass, field


_MONSTER_NAME = {
        'main' : ['#part#'*i for i in range(2,5)],
        'part': ['#sub_a#', '#sub_b##sub_a#'],
        'sub_a': '#a_vog##a_con#',
        'a_vog': ['a', 'e', 'i', 'o', 'u'],
        'a_con': ['l', 'z', 'k', 'w', 'm', 'n'],
        'sub_b': ['ch', 'x', 'k', 'd', 'm', 't', 'tr', 'th'],
        }


def monster_names():
    g = tracery.Grammar(_MONSTER_NAME)
    while True:
        yield g.flatten('#main#')


_INTRO_LETTER = {
            'main': ['#l1#. #l2#.', '#l2#. #l1#.'],
            'l1': [
                '#peço_desculpas# #pedindo#, #interlocutor#, #final#',
                '#interlocutor#, #peço_desculpas# #pedindo#, #final#',
                '#peço_desculpas# #pedindo#, #final#, #interlocutor#'],
            'interlocutor': ['meu #velho# #amigo#', '#velho# #amigo#', 'meu #amigo#'],
            'peço_desculpas': ['eu #peço_desculpas_multi#', 'eu #peço_desculpas_multi#, #peço_desculpas_multi#'],
            'peço_desculpas_multi': ['peço perdão', 'sinto muito', 'peço desculpas'],
            'pedindo': ['por estar te pedindo tanto', 'por ter que te pedir tanto', 'por deixar em teus ombros tal tarefa'],
            'amigo': ['amigo', 'companheiro'],
            'velho': ['velho', 'bom', 'saudoso', 'grande'],
            'há': ['há', 'tenho', 'sei'],
            'pedir': ['pedir', 'recorrer'],
            'final': ['mas não #há# mais a quem #pedir#', 'mas tenho de fazê-lo'],
            'l2': [
                'um #grade_erro# #foi_cometido#, e eu #não_posso# de #resolvê-lo#',
                '#foi_cometido# um #grade_erro#, e eu #não_posso# de #resolvê-lo#'
                ],
            'não_posso': ['não sou mais capaz', 'não posso mais', 'sou incapaz'],
            'resolvê-lo': ['resolvê-lo', 'corrigi-lo', 'fazê-lo correto', 'resolver ele', 'corrigir ele', 'desfazer ele', 'desfazê-lo'],
            'grade_erro': ['#grande# #erro#', '#erro# #grande#'],
            'grande': ['grande', 'terrível', 'fatal', 'horroroso'],
            'erro': ['erro', 'pecado', 'desacerto'],
            'foi_cometido': ['foi cometido', 'aconteceu', 'cometeu-se', 'veio a ser'],
        }


def intro_letter():
    g = tracery.Grammar(_INTRO_LETTER)
    while True:
        yield g.flatten('#main#')


_LOCATION_NAMES = {
            'main': ['#name#', '#prefix# #name#', '#name# #sufix#', '#prefix# #name# #sufix#'],
            'prefix': ['new', 'van'],
            'sufix': ['#direction#', '#altura#'],
            'direction': ['do sul', 'do norte', 'ocidental', 'oriental'],
            'altura': ['baixo', 'alto'],
            'name': '#start##silaba##end#',
            'start': ['h#vogal#', 'k#vogal#', '#vogal#', '#silaba#'],
            'end': ['', 'm', 'n', 'd', 'h'],
            'silaba': ['#silaba##silaba#', '#consoante##vogal#', '#consoante##end##vogal#', '#consoante##vogal#', '#consoante##vogal#'],
            'vogal': ['a', 'e', 'i', 'o', 'u'],
            'consoante': ['ff', 't', 'd', 'rr', 'c', 't', 'j', 'l', 'b', 'c', 'd', 'f', 'j', 'l', 'p', 'q', 'r', 's', 'v']
        }


def location_names():
    g = tracery.Grammar(_LOCATION_NAMES)
    while True:
        yield g.flatten('#main#')
_LOCATION_NAMES_GENERATOR = location_names()


class ContextualModifiers(Mapping):

    def __init__(self, grammar):
        self.grammar = grammar
        self.__norepeat = {}
        self.__norepeat_said = set()
        self.__mapping = {
            'norepeat': partial(self.norepeat),
            'gender': partial(self.gender)
        }


    def gender(self, gender, text): 
        return self.grammar.flatten(f'#{text}_{gender}#')


    def norepeat(self, text=None, group=None):
        symbols = self.grammar.symbols
        if group in symbols and isinstance(symbols[group].raw_rules, list):
            sym = symbols[group]
            raw = sym.raw_rules
            if len(raw) == 1 and raw[0] in symbols and raw[0] != group: 
                return self.norepeat(text, raw[0])
            if group not in self.__norepeat or not self.__norepeat[group]:
                self.__norepeat[group] = {i for i in raw}
            new_text = None
            while (new_text is None and self.__norepeat[group]):
                new_text = choice(tuple(self.__norepeat[group]))
                self.__norepeat[group] = self.__norepeat[group] - {new_text}
                if new_text in self.__norepeat_said:
                    new_text = None
            if new_text is None:
                self.reset_norepeat()
                return self.norepeat(text, group)
            self.__norepeat_said.add(new_text)
            return new_text
        else:
            return text

    def reset_norepeat(self):
        self.__norepeat = {}
        self.__norepeat_said = set()


    def __getitem__(self, key):
        return self.__mapping[key]

    def __iter__(self):
        return iter(self.__mapping)

    def __len__(self):
        return len(self.__mapping)


@dataclass(frozen=True)
class Substantive():
    word: str
    o: str
    um: str

    def raw(self, prefix):
        return {
                f'{prefix}': self.word,
                f'{prefix}_o': self.o,
                f'{prefix}_um': self.um,
                }

    @classmethod
    def make_male(cls, word):
        return cls(word, 'o', 'um')

    @classmethod
    def make_female(cls, word):
        return cls(word, 'a', 'uma')


@dataclass(frozen=True)
class Adjective():
    m: str
    ms: str
    f: str
    fs: str

    @classmethod
    def make(cls, rad, m=None, ms=None, f=None, fs=None):
        return Adjective(
                m = f'{rad}o' if m is None else m,
                ms = f'{rad}os' if ms is None else ms,
                f = f'{rad}a' if f is None else f,
                fs = f'{rad}as' if fs is None else fs
                )

    @classmethod
    def make_agender(cls, rad, rad_s=None, same=False):
        if same:
            rad_s = rad
        elif rad_s is None:
            rad_s = f'{rad}s'
        return Adjective(rad, rad_s, rad, rad_s)


@dataclass(frozen=True)
class Flavor():
    _adjectives: tuple

    def raw(self, adj = 'adjetivo'):
        return {
                f'{adj}_o': [a.m for a in self._adjectives],
                f'{adj}_os': [a.ms for a in self._adjectives],
                f'{adj}_a': [a.f for a in self._adjectives],
                f'{adj}_as': [a.fs for a in self._adjectives]
                }


    @classmethod
    @lru_cache
    def join(cls, a, b, *c):
        new =  cls(a._adjectives + b._adjectives)
        if c:
            return cls.join(new, *c)
        else:
            return new


_MAP_FLAVOR_LIST = [
        Flavor((
            Adjective.make('decrépit'),
            Adjective.make('decaíd'),
            Adjective.make('abandonad'),
            Adjective.make('descuidad'),
            Adjective.make('maltratad'),
            Adjective.make('castigad'))),
        Flavor((
            Adjective.make('sombri'),
            Adjective.make('escur'),
            Adjective.make('mal iluminad'),
            Adjective.make('obscur'),
            Adjective.make_agender('fúnebre'))),
        Flavor((
            Adjective.make('gótic'),
            Adjective.make('melancólic'),
            Adjective.make_agender('triste'),
            Adjective.make_agender('sufocante'))),
        Flavor((
            Adjective.make('isolad'),
            Adjective.make('solitári'),
            Adjective.make_agender('só'))),
        Flavor((
            Adjective.make('mal falad'),
            Adjective.make('maldit'),
            Adjective.make('amaldiçoad'),
            Adjective.make('assombrad'),
            Adjective.make('malign'),
            )),
        ]

_SECONDARY_FLAVOR_LIST = [
        Flavor((
            Adjective.make('empoeirad'),
            Adjective.make('suj'),
            Adjective.make('imund'),
            )),
        Flavor((
            Adjective.make('fri'),
            Adjective.make('gélid'),
            Adjective.make('gelad'),
            )),
        Flavor((
            Adjective.make('húmid'),
            Adjective.make('mofad'),
            )),
        Flavor((
            Adjective.make('pequen'),
            Adjective.make('claustrofóbic'),
            Adjective.make('apertad'),
            )),
        ]

_TERCIARY_FLAVOR_LIST = [
        Flavor((
            Adjective.make_agender('com pó se acumulando nas superfícies', same=True),
            Adjective.make_agender('com teias de aranha', same=True),
            )),
        Flavor((
            Adjective.make_agender('com goteiras', same=True),
            Adjective.make_agender('com poças d\'água', same=True),
            )),
        Flavor((
            Adjective.make_agender('com mofo', same=True),
            Adjective.make_agender('com cheiro de mofo', same=True),
            )),
        Flavor((
            Adjective.make_agender('com poças de sangue seco', same=True),
            Adjective.make_agender('com cheiro de sangue', same=True),
            )),
        Flavor((
            Adjective.make_agender('com um vento macabro', same=True),
            Adjective.make_agender('com uma brisa desagradável', same=True),
            )),
        Flavor((
            Adjective.make_agender('com cheiro de podre', same=True),
            Adjective.make_agender('com um cheiro desagradável', same=True),
            )),
        ]


def composed_map_flavor():
    return Flavor.join(*sample(_MAP_FLAVOR_LIST, 3))


@dataclass(frozen=True)
class BaseMapType():
    desc: tuple
    place_types: tuple

    def raw(self, prefix=''):
        return {
                 **choice(self.desc).raw(prefix)
                }

@dataclass(frozen=True)
class BasePlaceType():
    desc: 'Substantive'
    repeat: bool = False
    restrain: bool = False


map_type = BaseMapType(
        (
            Substantive.make_female('mansão'),
            Substantive.make_male('castelo'),
            Substantive.make_male('casarão'),
            ),
        (
            Substantive.make_female('cozinha'),
            Substantive.make_female('sala'),
            Substantive.make_female('sala de jantar'),
            Substantive.make_female('sala de estar'),
            Substantive.make_female('sala de Leitura'),
            Substantive.make_female('biblioteca'),
            Substantive.make_male('corredor'),
            Substantive.make_male('quarto de visitantes'),
            Substantive.make_male('quarto de empregados'),
            Substantive.make_male('quarto'),
            Substantive.make_male('atelie'),
            )
        )



@dataclass(frozen=True)
class Map():
    base_type: 'BaseMapType' = field(default=map_type, init=False)
    flavor: 'Flavor' = field(default_factory=composed_map_flavor, init=False)
    name: str = field(default_factory=lambda: next(_LOCATION_NAMES_GENERATOR), init=False)


class SuperContext():
    def __init__(self, base_description=None):
        self._raw_grammar = {'empty': ''}
        self._base_description = base_description
    
    @property
    def raw_grammar(self):
        return self._raw_grammar

    def make_grammar(self):
        g = tracery.Grammar(self.raw_grammar)
        g.add_modifiers(ContextualModifiers(g))
        return g

    @lru_cache
    def describe(self):
        grammar = self.make_grammar()
        desc = grammar.flatten(self._base_description)
        return desc.replace('\n', ' ').strip()

class Context(SuperContext):
    def __init__(self):
        super().__init__()

        self._map = MapContext(Map())


_MAP_BASE_DESCRIPTION ='''
#tipo_o# #tipo# #nome# é um lugar #empty.norepeat(adjetivo_o)# com seus muros
#empty.norepeat(adjetivo_os)# e seus portais #empty.norepeat(adjetivo_os)#.  As
paredes #empty.norepeat(adjetivo_as)# e #empty.norepeat(adjetivo_as)#, o piso e
as tábuas #empty.norepeat(adjetivo_as)#, os móveis
#empty.norepeat(adjetivo_os)#.  Tudo parece causar um medo primitivo, como se a
sua alma estivesse se tornando #empty.norepeat(adjetivo_a)# conforme você olha
para esta silhueta #empty.norepeat(adjetivo_a)#. Este não é o local onde você
queria estar.'''

class MapContext(SuperContext):
    def __init__(self, _map):
        super().__init__(_MAP_BASE_DESCRIPTION)
        self._raw_grammar['nome'] = _map.name
        self._raw_grammar.update(_map.flavor.raw())
        self._raw_grammar.update(_map.base_type.raw('tipo'))

        self._map = _map
        self.places = []

    def make_place(self):
        self.places.append(PlaceContext(self))
        return self.places[-1]


_PLACE_BASE_DESCRIPTION = ['''
        [temp:adjetivo_#tipo_o#] [temp2:adjetivo_comp_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)# e #empty.norepeat(temp2)#
        ''', '''
        [temp:adjetivo_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)#
        ''','''
        [temp2:adjetivo_comp_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)# #empty.norepeat(temp2)# ''']

class PlaceContext(SuperContext):
    def __init__(self, _map_context):

        super().__init__('#desc#')
        self._raw_grammar['desc'] = _PLACE_BASE_DESCRIPTION
        nome = choice(_map_context._map.base_type.place_types)
        self._raw_grammar.update(nome.raw('tipo'))

        flavor = choice(_SECONDARY_FLAVOR_LIST)
        self._raw_grammar.update(flavor.raw())

        flavor = choice(_TERCIARY_FLAVOR_LIST)
        self._raw_grammar.update(flavor.raw('adjetivo_comp'))

