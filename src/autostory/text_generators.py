from tracery import Grammar
from collections.abc import Mapping
from random import choice, sample, randint
from functools import partial, lru_cache
from typing import NamedTuple, NamedTupleMeta
from abc import ABC, abstractproperty

_MONSTER_NAME = {
        'main' : ['#part#'*i for i in range(2,5)],
        'part': ['#sub_a#', '#sub_b##sub_a#'],
        'sub_a': '#a_vog##a_con#',
        'a_vog': ['a', 'e', 'i', 'o', 'u'],
        'a_con': ['l', 'z', 'k', 'w', 'm', 'n'],
        'sub_b': ['ch', 'x', 'k', 'd', 'm', 't', 'tr', 'th'],
        }


def monster_names():
    g = Grammar(_MONSTER_NAME)
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
    g = Grammar(_INTRO_LETTER)
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
    g = Grammar(_LOCATION_NAMES)
    while True:
        yield g.flatten('#main#')


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


class Substantive(NamedTuple):
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


class Adjective(NamedTuple):
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


class _Flavor(NamedTuple):
    adjectives: tuple

    def raw(self, adj = 'adjetivo'):
        return {
                f'{adj}_o': [a.m for a in self.adjectives],
                f'{adj}_os': [a.ms for a in self.adjectives],
                f'{adj}_a': [a.f for a in self.adjectives],
                f'{adj}_as': [a.fs for a in self.adjectives]
                }

    @classmethod
    @lru_cache
    def join(cls, a, b, *c):
        new = cls(a.adjectives + b.adjectives)
        if c:
            return cls.join(new, *c)
        else:
            return new


_MAP_FLAVOR_LIST = (
        _Flavor((
            Adjective.make('decrépit'),
            Adjective.make('decaíd'),
            Adjective.make('abandonad'),
            Adjective.make('descuidad'),
            Adjective.make('maltratad'),
            Adjective.make('castigad'))),
        _Flavor((
            Adjective.make('sombri'),
            Adjective.make('escur'),
            Adjective.make('mal iluminad'),
            Adjective.make('obscur'),
            Adjective.make_agender('fúnebre'))),
        _Flavor((
            Adjective.make('gótic'),
            Adjective.make('melancólic'),
            Adjective.make_agender('triste'),
            Adjective.make_agender('sufocante'))),
        _Flavor((
            Adjective.make('isolad'),
            Adjective.make('solitári'),
            Adjective.make_agender('só'))),
        _Flavor((
            Adjective.make('mal falad'),
            Adjective.make('maldit'),
            Adjective.make('amaldiçoad'),
            Adjective.make('assombrad'),
            Adjective.make('malign'),
            )),
    )


_PLACE_FLAVOR_LIST = (
        _Flavor((
            Adjective.make('empoeirad'),
            Adjective.make('suj'),
            Adjective.make('imund'),
            )),
        _Flavor((
            Adjective.make('fri'),
            Adjective.make('gélid'),
            Adjective.make('gelad'),
            )),
        _Flavor((
            Adjective.make('húmid'),
            Adjective.make('mofad'),
            )),
        _Flavor((
            Adjective.make('pequen'),
            Adjective.make('claustrofóbic'),
            Adjective.make('apertad'),
            )),
        )


_SECONDATY_PLACE_FLAVOR_LIST = [
        _Flavor((
            Adjective.make_agender('com pó se acumulando nas superfícies', same=True),
            Adjective.make_agender('com teias de aranha', same=True),
            )),
        _Flavor((
            Adjective.make_agender('com goteiras', same=True),
            Adjective.make_agender('com poças d\'água', same=True),
            )),
        _Flavor((
            Adjective.make_agender('com mofo', same=True),
            Adjective.make_agender('com cheiro de mofo', same=True),
            )),
        _Flavor((
            Adjective.make_agender('com poças de sangue seco', same=True),
            Adjective.make_agender('com cheiro de sangue', same=True),
            )),
        _Flavor((
            Adjective.make_agender('com um vento macabro', same=True),
            Adjective.make_agender('com uma brisa desagradável', same=True),
            )),
        _Flavor((
            Adjective.make_agender('com cheiro de podre', same=True),
            Adjective.make_agender('com um cheiro desagradável', same=True),
            )),
        ]


class _MapType(NamedTuple):
    desc: tuple
    place_types: tuple

    def raw(self, prefix=''):
        return {
                 **choice(self.desc).raw(prefix)
                }


class _PlaceType(NamedTuple):
    desc: 'Substantive'
    decorations: tuple
    repeat: bool = False
    dead_end: bool = False


class _DecorationItem(NamedTuple):
    desc: 'Substantive'


_POLTRONA = _DecorationItem(
        Substantive.make_female('poltrona')
        )
_SOFA = _DecorationItem(
        Substantive.make_male('sofa')
        )
_CADEIRA = _DecorationItem(
        Substantive.make_male('cadeira')
        )
_MESA = _DecorationItem(
        Substantive.make_female('mesa')
        )
_MESA_DE_CENTRO = _DecorationItem(
        Substantive.make_female('mesa de centro')
        )
_MESA_DE_CABECEIRA = _DecorationItem(
        Substantive.make_female('mesa de cabeceira')
        )
_PIA = _DecorationItem(
        Substantive.make_female('pia')
        )
_LAREIRA = _DecorationItem(
        Substantive.make_female('lareira')
        )
_FOGAO = _DecorationItem(
        Substantive.make_male('fogão')
        )
_CAMA = _DecorationItem(
        Substantive.make_female('cama')
        )
_ESTANTE = _DecorationItem(
        Substantive.make_female('estante')
        )
_ESPELHO = _DecorationItem(
        Substantive.make_male('espelho')
        )


################################################################################


_COZINHA = _PlaceType(
        Substantive.make_female('cozinha'),
        (_MESA, _PIA, _FOGAO, _LAREIRA, _ESTANTE))
_SALA = _PlaceType(
        Substantive.make_female('sala'),
        (_POLTRONA, _SOFA, _MESA_DE_CENTRO, _ESTANTE, _LAREIRA),
        repeat = True)
_SALA_DE_JANTAR = _PlaceType(
        Substantive.make_female('sala de jantar'),
        (_CADEIRA, _MESA, _ESTANTE, _LAREIRA))
_SALA_DE_ESTAR = _PlaceType(
        Substantive.make_female('sala de estar'),
        (_POLTRONA, _SOFA, _MESA_DE_CENTRO, _ESTANTE, _LAREIRA))
_SALA_DE_LEITURA = _PlaceType(
        Substantive.make_female('sala de Leitura'),
        (_POLTRONA, _SOFA, _MESA_DE_CENTRO, _ESTANTE, _LAREIRA))
_BIBLIOTECA = _PlaceType(
        Substantive.make_female('biblioteca'),
        (_POLTRONA, _SOFA, _MESA_DE_CENTRO, _ESTANTE, _LAREIRA, _CADEIRA))
_CORREDOR = _PlaceType(
        Substantive.make_male('corredor'),
        (), #TODO
        repeat = True)
_GALERIA = _PlaceType(
        Substantive.make_female('galeria'),
        (), #TODO
        repeat = True)
_QUARTO_DE_VISITANTES = _PlaceType(
        Substantive.make_male('quarto de visitantes'),
        (_CAMA, _MESA_DE_CABECEIRA, _LAREIRA, _CADEIRA, _POLTRONA, 
            _ESTANTE, _MESA_DE_CENTRO, _ESPELHO),
        repeat = True)
_QUARTO_DE_EMPREGADOS = _PlaceType(
        Substantive.make_male('quarto de empregados'),
        (_CAMA, _MESA_DE_CABECEIRA, _CADEIRA, _ESTANTE),
        dead_end = True)
_QUARTO = _PlaceType(
        Substantive.make_male('quarto'),
        (_CAMA, _MESA_DE_CABECEIRA, _LAREIRA, _CADEIRA, _POLTRONA, 
            _ESTANTE, _MESA_DE_CENTRO, _ESPELHO),
        repeat = True)
_CLOSET = _PlaceType(
        Substantive.make_male('closet'),
        (_ESTANTE, _ESPELHO),
        repeat = True,
        dead_end = True)
_DEPOSITO = _PlaceType(
        Substantive.make_male('Depósito'),
        (_ESTANTE,),
        repeat = True,
        dead_end = True)
_SOTAO = _PlaceType(
        Substantive.make_male('sótão'),
        (), #TODO
        dead_end = True)
_PORAO = _PlaceType(
        Substantive.make_male('Porão'),
        (), #TODO
        dead_end = True)
_ATELIE = _PlaceType(
        Substantive.make_male('atelie'),
        ()) #TODO


_MAP_TYPE = _MapType(
            (
                Substantive.make_female('mansão'),
                Substantive.make_male('castelo'),
                Substantive.make_male('casarão'),
                ),
            (
                _COZINHA,
                _SALA,
                _SALA_DE_JANTAR,
                _SALA_DE_ESTAR,
                _SALA_DE_LEITURA,
                _BIBLIOTECA,
                _CORREDOR,
                _GALERIA,
                _QUARTO_DE_VISITANTES,
                _QUARTO_DE_EMPREGADOS,
                _QUARTO,
                _CLOSET,
                _DEPOSITO,
                _SOTAO,
                _PORAO,
                _ATELIE
            )
        )


class GrammerMakebla(ABC):
    @abstractproperty
    def base_description(self):
        pass

    @abstractproperty
    def raw_grammar(self):
        pass


_MAP_BASE_DESCRIPTION ='''
#tipo_o# #tipo# #nome# é um lugar #empty.norepeat(adjetivo_o)# com seus muros
#empty.norepeat(adjetivo_os)# e seus portais #empty.norepeat(adjetivo_os)#. As
paredes #empty.norepeat(adjetivo_as)# e #empty.norepeat(adjetivo_as)#, o piso e
as tábuas #empty.norepeat(adjetivo_as)#, os móveis
#empty.norepeat(adjetivo_os)#. Tudo parece causar um medo primitivo, como se a
sua alma estivesse se tornando #empty.norepeat(adjetivo_a)# conforme você olha
para esta silhueta #empty.norepeat(adjetivo_a)#. Este não é o local onde você
queria estar.'''


class Map(NamedTuple):
    base_type: '_MapType'
    flavor: '_Flavor'
    name: str
    base_description: str

    _LOCATION_NAMES_GENERATOR = location_names()

    @classmethod
    def _composed_map_flavor(cls):
        return _Flavor.join(*sample(_MAP_FLAVOR_LIST, 3))

    @classmethod
    def make(cls):
        base_type: '_MapType' = _MAP_TYPE
        flavor: '_Flavor' = cls._composed_map_flavor()
        name: str = next(cls._LOCATION_NAMES_GENERATOR)

        return cls(
                base_type=base_type,
                flavor=flavor,
                name=name,
                base_description=_MAP_BASE_DESCRIPTION)

    def make_place(self):
        place_type = choice(self.base_type.place_types) 
        return Place.make(place_type)


    @property
    @lru_cache
    def raw_grammar(self):
        return {
                'empty': '',
                'nome': self.name,
                **self.flavor.raw(),
                **self.base_type.raw('tipo')
                }

GrammerMakebla.register(Map)

_PLACE_BASE_DESCRIPTION = ['''
        [temp:adjetivo_#tipo_o#] [temp2:adjetivo_comp_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)# e #empty.norepeat(temp2)#. ''', 
        '''[temp:adjetivo_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)#. ''',
        '''[temp2:adjetivo_comp_#tipo_o#] #tipo_um# #tipo# #empty.norepeat(temp)# #empty.norepeat(temp2)#.''']


class Place(NamedTuple):

    nome:str
    place_type: _PlaceType
    flavor_sec: _Flavor
    flavor_ter: _Flavor
    decorations: tuple
    base_description: str = '#desc##decorations#'

    @classmethod
    def make(cls, place_type):
        nome = place_type.desc
        flavor_sec = choice(_PLACE_FLAVOR_LIST)
        flavor_ter = choice(_SECONDATY_PLACE_FLAVOR_LIST)

        qtd_decorations = randint(0, len(place_type.decorations))
        decorations = tuple(sample(place_type.decorations, k=qtd_decorations))

        return cls(
                nome = nome,
                place_type = place_type,
                flavor_sec = flavor_sec,
                flavor_ter = flavor_ter,
                decorations = decorations
                )

    @property
    def raw_grammar(self):
        _raw_grammar = {'empty': ''}
        _raw_grammar['desc'] = _PLACE_BASE_DESCRIPTION

        if (self.decorations):
            listed_decoration = '; '.join(map(lambda d: f'{d.desc.um} {d.desc.word}' ,self.decorations))
            _raw_grammar['decorations'] = ' onde você pode ver ' + listed_decoration
        else:
            _raw_grammar['decorations'] = ''

        _raw_grammar.update(self.nome.raw('tipo'))
        _raw_grammar.update(self.flavor_sec.raw('adjetivo'))
        _raw_grammar.update(self.flavor_ter.raw('adjetivo_comp'))
        return _raw_grammar

GrammerMakebla.register(Map)

class Context(NamedTuple):
    map: 'Map' = Map.make()


def make_grammar(grammerMakebla: GrammerMakebla):
    g = Grammar(grammerMakebla.raw_grammar)
    g.add_modifiers(ContextualModifiers(g))
    return g

@lru_cache
def describe(grammerMakebla: GrammerMakebla):
    grammar = make_grammar(grammerMakebla)
    desc = grammar.flatten(grammerMakebla.base_description)
    return desc.replace('\n', ' ').strip()
