from tracery import Grammar
from collections.abc import Mapping
from random import choice, sample, randint
from functools import partial, lru_cache
from typing import NamedTuple, NamedTupleMeta
from abc import ABC, abstractproperty
import typing


import random


class GrammerMakebla(ABC):
    @abstractproperty
    def base_description(self):
        pass

    @abstractproperty
    def grammar(self):
        pass

@lru_cache
def make_grammar(grammerMakebla: GrammerMakebla):
    return grammerMakebla.grammar


def describe(grammerMakebla: GrammerMakebla):
    grammar = make_grammar(grammerMakebla)
    desc = grammar.flatten(grammerMakebla.base_description)
    return desc.replace('\n', ' ').strip()


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

    def __init__(self, grammar, context=None):
        self.grammar = grammar
        self.context = context
        self.__mapping = {
            'norepeat': partial(self.norepeat),
            'gender': partial(self.gender)
        }

    def gender(self, gender, text): 
        return self.grammar.flatten(f'#{text}_{gender}#')

    def norepeat(self, text=None, group=None):
        symbols = self.grammar.symbols

        if group not in symbols or not isinstance(symbols[group].raw_rules, list):
            return text
        
        options = symbols[group].raw_rules
        if len(options) == 1 and options[0] in symbols and options[0] != group: 
            # Sometimes the text to be not repeated is nested to treat gender
            # I know it is not pretty nut I am neither and I'm not complaining
            return self.norepeat(text, options[0])
        return self.context.norepeat(options)


    def reset_norepeat(self):
        self.context._reset_norepeat_said()

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

    def raw(self, prefix, context=None):
        rw = {
                f'{prefix}': self.word,
                f'{prefix}_o': self.o,
                f'{prefix}_um': self.um,
                }
        if context:
            context._register_norepeat_map(set(rw.values()))
        return rw

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
    def make(cls, rad=None, m=None, ms=None, f=None, fs=None):
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
    

    @classmethod
    def make_format(cls, _format, m='o', ms='os', f='a', fs='as'):
        return Adjective(_format(m), _format(ms), _format(f), _format(fs))


class _Flavor(NamedTuple):
    adjectives: typing.Tuple['Adjective'] = tuple()

    def raw(self, adj = 'adjetivo', context=None):
        m  = []
        ms = []
        f  = []
        fs = []

        for a in self.adjectives:
            m.append(a.m)
            ms.append(a.ms)
            f.append(a.f)
            fs.append(a.fs)
            if context:
                context._register_norepeat_map(set(a))
                
        rw = {
                f'{adj}_o':  m,
                f'{adj}_os': ms,
                f'{adj}_a':  f,
                f'{adj}_as': fs
                }
        return rw

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
    desc: typing.Tuple['Substantive']
    place_types: typing.Tuple['_PlaceType']

    def raw(self, prefix='', context=None):
        return {
                 **choice(self.desc).raw(prefix, context=context)
                }


class _PlaceType(NamedTuple):
    desc: 'Substantive'
    decorations: typing.Tuple[typing.Tuple[typing.Optional['_DecorationItemType']]]
    repeat: bool = False
    dead_end: bool = False


class _DecorationItemType(NamedTuple):
    desc: 'Substantive'
    flavor_list: typing.Tuple['_Flavor'] = None


_BASE_DECORATION_FLAVOR = _Flavor((
        Adjective.make('suj'),
        Adjective.make('muito suj'),
        Adjective.make('imund'),
        Adjective.make('velh'),
        Adjective.make('muito velh'),
        Adjective.make('empoeirad'),
        Adjective.make('muito empoeirad'),
        Adjective.make('maltratad'),
        Adjective.make('esquecid'),
        Adjective.make('abadonad'),
        Adjective.make('nojent'),
        Adjective.make_agender('deplorável', same=True),
        Adjective.make_format(lambda g: f'que parece{g[0]} que est{g[1]} suj{g[2]} a muito tempo',
            m=('', 'á', 'o'), ms=('m', 'ão', 'o'), f=('', 'á', 'a'), fs=('m', 'ão', 'as')),
        Adjective.make_format(lambda g: f'que parece{g[0]} que não {g[1]} limp{g[2]} a muito tempo',
            m=('', 'é', 'o'), ms=('m', 'são', 'o'), f=('', 'é', 'a'), fs=('m', 'são', 'as')),
    ))


_WOODEN_DECORATION_FLAVOR = _Flavor((
        Adjective.make_agender('de madeira', same=True),
        Adjective.make_agender('de madeira podre', same=True),
        Adjective.make_agender('de madeira maciça', same=True),
        Adjective.make_format(lambda g: f'feit{g} de madeira'),
        Adjective.make_format(lambda g: f' que feit{g} de madeira podre'),
        Adjective.make_agender('com lascas faltando', same=True),
        Adjective.make_agender('que está com lascas faltando', same=True),
        Adjective.make('lascad'),
        Adjective.make_agender('frágil', 'frágeis'),
    ))


_FABRIC_DECORATION_FLAVOR = _Flavor((
        Adjective.make_agender('de tecido', same=True),
        Adjective.make_format(lambda g: f'feit{g} de tecido'),
        Adjective.make_format(lambda g: f'de tecido e chei{g} de rasgos'),
        Adjective.make_format(lambda g: f'chei{g} de rasgos'),
        Adjective.make_format(lambda g: f'chei{g} de manchas'),
        Adjective.make_agender('com manchas', same=True),
        Adjective.make_agender('com rasgos', same=True),
        Adjective.make_agender('com furos', same=True),
        Adjective.make('mofad'),
    ))


_USEBLAE_DECORATION_FLAVOR = _Flavor((
        Adjective.make_agender('com marcas de uso', same=True),
        Adjective.make_agender('com muitas marcas de uso', same=True),
        Adjective.make_agender('que parece estar sem uso a anos', same=True),
        Adjective.make_agender('que parece que ninguém usa a muito tempo', same=True),
        Adjective.make_format(lambda g: f'que parece{g[0]} que {g[1]} muito usad{g[2]}',
            m=('', 'foi', 'o'), ms=('m', 'foram', 'o'), f=('', 'foi', 'a'), fs=('m', 'foram', 'as')),
        Adjective.make_format(lambda g: f'que parece{g[0]} que não {g[1]} usad{g[2]} a muito tempo',
            m=('', 'é', 'o'), ms=('m', 'são', 'o'), f=('', 'é', 'a'), fs=('m', 'são', 'as')),
        Adjective.make_format(lambda g: f'abandonad{g} a muito tempo'),
        Adjective.make_format(lambda g: f'que foi abandonad{g} a muito tempo'),
        Adjective.make_format(lambda g: f'replet{g} de marcas de uso'),
        Adjective.make_agender(f'que ninguém usa a muito tempo', same=True),
    ))


_ART_DECORATION_FLAVOR = _Flavor((
        Adjective.make_agender('de péssimo gosto', same=True),
        Adjective.make('macabr'),
        Adjective.make('horroros'),
        Adjective.make('sinistr'),
        Adjective.make('macabr'),
        Adjective.make('horroros'),
        Adjective.make('sinistr'),
        Adjective.make('bastante macabr'),
        Adjective.make('bastante horroros'),
        Adjective.make('bastante sinistr'),
        Adjective.make('muito macabr'),
        Adjective.make('muito horroros'),
        Adjective.make('muito sinistr'),
        Adjective.make_format(lambda g: f'atormentador{g}', m='', ms='es'),
        Adjective.make_format(lambda g: f'atormentador{g}', m='', ms='es'),
        Adjective.make_format(lambda g: f'bastante atormentador{g}', m='', ms='es'),
        Adjective.make_format(lambda g: f'muito atormentador{g}', m='', ms='es'),
    ))


####


_POLTRONA = _DecorationItemType(
        Substantive.make_female('poltrona'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _FABRIC_DECORATION_FLAVOR,)
        )
_SOFA = _DecorationItemType(
        Substantive.make_male('sofa'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _FABRIC_DECORATION_FLAVOR,)
        )
_CADEIRA = _DecorationItemType(
        Substantive.make_female('cadeira'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_MESA = _DecorationItemType(
        Substantive.make_female('mesa'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_MESA_DE_CENTRO = _DecorationItemType(
        Substantive.make_female('mesa de centro'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_MESA_DE_CABECEIRA = _DecorationItemType(
        Substantive.make_female('mesa de cabeceira'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_PIA = _DecorationItemType(
        Substantive.make_female('pia'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,)
        )
_LAREIRA = _DecorationItemType(
        Substantive.make_female('lareira'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,)
        )
_FOGAO = _DecorationItemType(
        Substantive.make_male('fogão'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,)
        )
_CAMA = _DecorationItemType(
        Substantive.make_female('cama'),
        (
            _BASE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _FABRIC_DECORATION_FLAVOR,)
        )
_ESTANTE = _DecorationItemType(
        Substantive.make_female('estante'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_ARMARIO = _DecorationItemType(
        Substantive.make_male('armario'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_CRISTALEIRA = _DecorationItemType(
        Substantive.make_female('cristaleira'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,)
        )
_ESPELHO = _DecorationItemType(
        Substantive.make_male('espelho'),
        (
            _BASE_DECORATION_FLAVOR,)
        )
_QUADRO = _DecorationItemType(
        Substantive.make_male('quadro'),
        (
            _BASE_DECORATION_FLAVOR,
            _WOODEN_DECORATION_FLAVOR,
            _ART_DECORATION_FLAVOR,
            _ART_DECORATION_FLAVOR,)
        )
_TAPETE = _DecorationItemType(
        Substantive.make_male('tapete'),
        (
            _BASE_DECORATION_FLAVOR,
            _USEBLAE_DECORATION_FLAVOR,
            _FABRIC_DECORATION_FLAVOR,)
        )
_BUSTO = _DecorationItemType(
        Substantive.make_male('busto'),
        (
            _BASE_DECORATION_FLAVOR,
            _ART_DECORATION_FLAVOR,)
        )
_LUSTRE = _DecorationItemType(
        Substantive.make_male('lustre'),
        (
            _BASE_DECORATION_FLAVOR,)
        )


################################################################################



_COZINHA = _PlaceType(
        Substantive.make_female('cozinha'),
        (
            (None, _MESA,),
            (_PIA,),
            (_LAREIRA, _FOGAO,),
            (_ESTANTE, _CRISTALEIRA, _ARMARIO,),
            )
        )
_SALA = _PlaceType(
        Substantive.make_female('sala'),
        (
            (_SOFA,),
            (_LAREIRA,),
            (None, _POLTRONA,),
            (None, _MESA_DE_CENTRO,),
            (None, _CRISTALEIRA, _ESTANTE, _ARMARIO,),
            (None, _QUADRO,),
            (None, _TAPETE,),
            (None, None, _BUSTO,),
            (None, None, _LUSTRE,),
            ),
        repeat = True
        )
_SALA_DE_JANTAR = _PlaceType(
        Substantive.make_female('sala de jantar'),
        (
            (_CADEIRA,),
            (_MESA,),
            (None, _ESTANTE, _ARMARIO, _CRISTALEIRA,),
            (None, _LAREIRA,),
            )
        )
_SALA_DE_ESTAR = _PlaceType(
        Substantive.make_female('sala de estar'),
        (
            (_POLTRONA,),
            (_SOFA,),
            (_MESA_DE_CENTRO,),
            (None, _CRISTALEIRA, _ARMARIO, _ESTANTE,),
            (None, None, _LUSTRE, _LAREIRA, _LAREIRA,),
            (None, _BUSTO, _QUADRO, _BUSTO, _QUADRO,),
            (None, None, None, _TAPETE,),
            ),
        )
_SALA_DE_LEITURA = _PlaceType(
        Substantive.make_female('sala de Leitura'),
        (
            (_LAREIRA,),
            (_POLTRONA,),
            (None, _SOFA,),
            (None, _MESA_DE_CENTRO,),
            (None, _ARMARIO, _ESTANTE, _ESTANTE,),
            (None, _QUADRO, _QUADRO,),
            (None, _BUSTO, _BUSTO,),
            (None, None, _TAPETE,),
            (None, None, None, _LUSTRE,),
            )
        )
_BIBLIOTECA = _PlaceType(
        Substantive.make_female('biblioteca'),
        (
            (_POLTRONA,),
            (_LAREIRA,),
            (_MESA_DE_CENTRO,),
            (_ESTANTE,),
            (None, _SOFA,),
            (None, _ARMARIO,),
            (None, _CADEIRA,),
            (None, _QUADRO, _QUADRO,),
            (None, _BUSTO, _BUSTO,),
            (None, None, _TAPETE,),
            (None, None, _LUSTRE,),
            (None, None, None, _MESA,),
            )
        )
_CORREDOR = _PlaceType(
        Substantive.make_male('corredor'),
        (
            (_QUADRO,),
            (None, _TAPETE,),
            (None, _BUSTO,),
            (None, _MESA_DE_CENTRO,),
            (None, None, _LUSTRE,),
            ),
        repeat = True
        )
_GALERIA = _PlaceType(
        Substantive.make_female('galeria'),
        (
            (None, _LAREIRA,),
            (None, _TAPETE,),
            (None, _MESA_DE_CENTRO,),
            ),
        repeat = True)
_QUARTO_DE_VISITANTES = _PlaceType(
        Substantive.make_male('quarto de visitantes'),
        (
            (_CAMA,),
            (_MESA_DE_CABECEIRA,),
            (None, _LAREIRA,),
            (None, _ESPELHO, _CADEIRA,),
            (None, _SOFA, _POLTRONA,),
            (None, _ARMARIO, _ESTANTE,),
            (None, _MESA_DE_CENTRO,),
            ),
        repeat = True)
_QUARTO_DE_EMPREGADOS = _PlaceType(
        Substantive.make_male('quarto de empregados'),
        (
            (_CAMA,),
            (None, _MESA_DE_CABECEIRA,),
            (None, _CADEIRA,),
            (None, _ARMARIO, _ESTANTE,),
            ),
        dead_end = True)
_QUARTO = _PlaceType(
        Substantive.make_male('quarto'),
        (
            (_CAMA,),
            (_MESA_DE_CABECEIRA,),
            (None, _LAREIRA,),
            (None, _CADEIRA,),
            (None, _SOFA, _POLTRONA,),
            (None, _ARMARIO, _ESTANTE,),
            (None, _MESA_DE_CENTRO,),
            (None, _ESPELHO,),
            (None, _QUADRO,),
            (None, _TAPETE,)
            ),
        repeat = True)
_CLOSET = _PlaceType(
        Substantive.make_male('closet'),
        (
            (None, _ESTANTE,),
            (_ARMARIO,),
            (_ESPELHO,)
            ),
        repeat = True,
        dead_end = True)
_DEPOSITO = _PlaceType(
        Substantive.make_male('Depósito'),
        (
            (None, _ESTANTE,),
            (None, _ARMARIO,)
            ),
        repeat = True,
        dead_end = True)
_SOTAO = _PlaceType(
        Substantive.make_male('sótão'),
        (
            (None, _CAMA,),
            (None, _MESA_DE_CABECEIRA,),
            (None, _CADEIRA,),
            (None, _POLTRONA,),
            (None, _SOFA,),
            (None, _ESTANTE,),
            (None, _ARMARIO,),
            (None, _MESA_DE_CENTRO,),
            (None, _ESPELHO,),
            (None, _QUADRO,),
            (None, _TAPETE,),
            (None, _CRISTALEIRA,)
            ),
        dead_end = True)
_PORAO = _PlaceType(
        Substantive.make_male('Porão'),
        (
            (None, _CAMA,),
            (None, _MESA_DE_CABECEIRA,),
            (None, _CADEIRA,),
            (None, _POLTRONA,),
            (None, _SOFA,),
            (None, _ESTANTE,),
            (None, _ARMARIO,),
            (None, _MESA_DE_CENTRO,),
            (None, _ESPELHO,),
            (None, _QUADRO,),
            (None, _TAPETE,),
            (None, _CRISTALEIRA,)
            ),
        dead_end = True)
_ATELIE = _PlaceType(
        Substantive.make_male('atelie'),
        (
            (None, _QUADRO,),
            (None, _ESPELHO,),
            (None, _ARMARIO,),
            (None, _MESA,),
            (None, _TAPETE,),
            (None, _BUSTO,)
            )
        )


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
    context: 'Context'
    base_type: '_MapType'
    flavor: '_Flavor'
    name: str
    base_description: str

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
                name=name,
                base_description=_MAP_BASE_DESCRIPTION)

    def make_place(self):
        place_type = choice(self.base_type.place_types) 
        return Place.make(place_type, self.context)


    @property
    @lru_cache
    def __raw_grammar(self):
        return {
                'empty': '',
                'nome': self.name,
                **self.flavor.raw(context=self.context),
                **self.base_type.raw('tipo', context=self.context)
                }

    @property
    @lru_cache
    def grammar(self):
        g = Grammar(self.__raw_grammar)
        g.add_modifiers(ContextualModifiers(g, self.context))
        return g

GrammerMakebla.register(Map)


class DecorationItem(NamedTuple):
    decoration_type: '_DecorationItemType'
    context: 'Context'

    @property
    @lru_cache
    def desc(self):
        return self.decoration_type.desc

    @property
    @lru_cache
    def __raw_grammar(self):
        deco = self.decoration_type
        return {
                'empty': '',
                **deco.desc.raw('nome', context=self.context),
                **choice(deco.flavor_list).raw(context=self.context),
                'main': '#nome_um# #nome##_adjetivo#',
                '_adjetivo': '[adj:adjetivo_#nome_o#]#_sub_adj#',
                '_sub_adj': ['', ' #empty.norepeat(adj)#', ' #empty.norepeat(adj)#']
                }

    @property
    @lru_cache
    def base_description(self):
        return '#main#'

    @property
    @lru_cache
    def grammar(self):
        g = Grammar(self.__raw_grammar)
        g.add_modifiers(ContextualModifiers(g, self.context))
        return g

GrammerMakebla.register(DecorationItem)


_PLACE_BASE_DESCRIPTION = ['''
        [temp:adjetivo_#tipo_o#] [temp2:adjetivo_comp_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)# e #empty.norepeat(temp2)#. ''', 
        '''[temp:adjetivo_#tipo_o#]
        #tipo_um# #tipo# #empty.norepeat(temp)#. ''',
        '''[temp2:adjetivo_comp_#tipo_o#] #tipo_um# #tipo# #empty.norepeat(temp)# #empty.norepeat(temp2)#.''']


class Place(NamedTuple):
    context: 'Context'
    nome:str
    place_type: _PlaceType
    flavor_sec: _Flavor
    flavor_ter: _Flavor
    decorations: typing.Tuple['DecorationItem']
    base_description: str = '#desc##decorations#'

    @classmethod
    def make(cls, place_type, context):
        nome = place_type.desc
        flavor_sec = choice(_PLACE_FLAVOR_LIST)
        flavor_ter = choice(_SECONDATY_PLACE_FLAVOR_LIST)

        decorations = tuple(DecorationItem(deco, context) for deco in map(choice, place_type.decorations) if deco is not None)

        return cls(
                context = context,
                nome = nome,
                place_type = place_type,
                flavor_sec = flavor_sec,
                flavor_ter = flavor_ter,
                decorations = decorations
                )

    @property
    def __raw_grammar(self):
        _raw_grammar = {'empty': ''}
        _raw_grammar['desc'] = _PLACE_BASE_DESCRIPTION

        if (self.decorations):
            decor_desc_tuple = tuple(describe(d) for d in self.decorations)
            if (len(decor_desc_tuple) > 1):
                decor_desc_tuple = tuple(sorted(decor_desc_tuple, key=len))
                listed_decoration = ', '.join(decor_desc_tuple[:-1]) + f' e {decor_desc_tuple[-1]}'
            else:
                listed_decoration = decor_desc_tuple[0]
            _raw_grammar['decorations'] = ' onde você pode ver ' + listed_decoration
        else:
            _raw_grammar['decorations'] = ''

        _raw_grammar.update(self.nome.raw('tipo'))
        _raw_grammar.update(self.flavor_sec.raw('adjetivo'))
        _raw_grammar.update(self.flavor_ter.raw('adjetivo_comp'))
        return _raw_grammar

    @property
    @lru_cache
    def grammar(self):
        g = Grammar(self.__raw_grammar)
        g.add_modifiers(ContextualModifiers(g, self.context))
        return g


GrammerMakebla.register(Map)


class Context():
    def __init__(self):
        self.map = Map.make(self)
        self._norepeat_said = set()
        self._norepeat_map = list()

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
                self._norepeat_said |= group
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

