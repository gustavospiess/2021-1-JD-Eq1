from random import choice

from typing import (
        NamedTuple,
        Tuple,
        Optional,
        )

from functools import lru_cache

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


class _Flavor(NamedTuple):
    adjectives: Tuple['Adjective'] = tuple()

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
    desc: Tuple['Substantive']
    place_types: Tuple['_PlaceType']
    passage_types: Tuple['_PassageType']

    def raw(self, prefix='', context=None):
        return {
                 **choice(self.desc).raw(prefix, context=context)
                }


class _PlaceType(NamedTuple):
    desc: 'Substantive'
    decorations: Tuple[Tuple[Optional['_DecorationItemType']]]
    repeat: bool = False


class _ItemType(NamedTuple):
    desc: 'Substantive'
    flavor_list: Tuple['_Flavor']


class _KeyType(NamedTuple):
    desc: 'Substantive'
    flavor_list: Tuple['_Flavor']


class _PassageType(NamedTuple):
    a_side: 'Substantive'
    b_side: 'Substantive'
    flavor_list: Tuple['_Flavor']
    key_type: _KeyType = None

    @classmethod
    def make_unsided(cls, desc: 'Substantive', *args, **kwargs):

        return cls(
                a_side = desc,
                b_side = desc,
                *args,
                **kwargs
                )


class _DecorationItemType(_ItemType):
    pass


################################################################################


_NULL_ITEM_FLAVOR = _Flavor((Adjective('', '', '', ''),))

_BASE_ITEM_FLAVOR = _Flavor((
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
    Adjective.make_agender('deplorável', rad_s='deploráveis'),
    Adjective.make_format(lambda g: f'que parece{g[0]} que est{g[1]} suj{g[2]} a muito tempo',
        m=('', 'á', 'o'), ms=('m', 'ão', 'o'), f=('', 'á', 'a'), fs=('m', 'ão', 'as')),
    Adjective.make_format(lambda g: f'que parece{g[0]} que não {g[1]} limp{g[2]} a muito tempo',
        m=('', 'é', 'o'), ms=('m', 'são', 'o'), f=('', 'é', 'a'), fs=('m', 'são', 'as')),
    ))
_WOODEN_ITEM_FLAVOR = _Flavor((
    Adjective.make_agender('de madeira', same=True),
    Adjective.make_agender('de madeira podre', same=True),
    Adjective.make_agender('de madeira maciça', same=True),
    Adjective.make_format(lambda g: f'feit{g} de madeira'),
    Adjective.make_format(lambda g: f' que é feit{g} de madeira podre'),
    Adjective.make_agender('com lascas faltando', same=True),
    Adjective.make_agender('que está com lascas faltando', same=True),
    Adjective.make('lascad'),
    ))
_METAL_ITEM_FLAVOR = _Flavor((
    Adjective.make_agender('de metal', same=True),
    Adjective.make_agender('de ferro', same=True),
    Adjective.make_format(lambda g: f'enferrujad{g}'),
    Adjective.make_format(lambda g: f'cobert{g} de ferrugem'),
    Adjective.make_format(lambda g: f'feit{g} metal'),
    Adjective.make_format(lambda g: f' que é feit{g} de metal'),
    Adjective.make_agender('brilhante', same=True),
    Adjective.make_agender('frágil', 'frágeis'),
    Adjective.make_agender('resistente'),
    ))
_FABRIC_ITEM_FLAVOR = _Flavor((
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
_USEBLAE_ITEM_FLAVOR = _Flavor((
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
_ART_ITEM_FLAVOR = _Flavor((
    Adjective.make_agender('de péssimo gosto', same=True),
    Adjective.make('macabr'),
    Adjective.make('horroros'),
    Adjective.make('sinistr'),
    Adjective.make('macabr'),
    Adjective.make('horroros'),
    Adjective.make('sinistr'),
    Adjective.make('bastante macabr'),
    Adjective.make('bastante sinistr'),
    Adjective.make_format(lambda g: f'atormentador{g}', m='', ms='es'),
    Adjective.make_format(lambda g: f'atormentador{g}', m='', ms='es'),
    Adjective.make_format(lambda g: f'bastante atormentador{g}', m='', ms='es'),
    Adjective.make_format(lambda g: f'muito atormentador{g}', m='', ms='es'),
    ))
_DELICATE_ITEM_FLAVOR = _Flavor((
    Adjective.make('delicad'),
    Adjective.make_agender('frágil', 'frágeis'),
    ))


################################################################################


_CHAVE_BASICA = _KeyType(
        desc = Substantive.make_female('chave'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            # _WOODEN_ITEM_FLAVOR,
            # _ART_ITEM_FLAVOR,
            ),
        )


################################################################################


_ESCADA = _PassageType.make_unsided(
        desc = Substantive.make_female('escada'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _DELICATE_ITEM_FLAVOR,
            ),
        )
_PASSAGEM = _PassageType.make_unsided(
        desc = Substantive.make_female('passagem'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            _DELICATE_ITEM_FLAVOR,
            ),
        )
_PASSAGEM_ADORNADA = _PassageType.make_unsided(
        desc = Substantive.make_female('passagem adornada'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            _DELICATE_ITEM_FLAVOR,
            ),
        )
_PORTA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            _DELICATE_ITEM_FLAVOR,
            ),
        )
_PORTA_TRANCADA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta trancada'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA
        )
_PORTA_DUPLA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta dupla'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            _DELICATE_ITEM_FLAVOR,
            ),
        )
_PORTA_DUPLA_TRANCADA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta dupla trancada'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA
        )
_PORTA_ADORNADA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta adornada'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA
        )
_PORTA_ADORNADA_TRANCADA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta adornada e trancada'),
        flavor_list = (
            _USEBLAE_ITEM_FLAVOR,
            _BASE_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,
            _METAL_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA
        )
_PASSAGEM_SECRETA_LIVROS = _PassageType.make_unsided(
        desc = Substantive.make_female('estante de livros'),
        flavor_list = (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA #TODO
        )
_PASSAGEM_SECRETA_QUADRO = _PassageType.make_unsided(#TODO two sides
        desc = Substantive.make_male('quadro'),
        flavor_list = (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA #TODO
        )
_PORTA_TIJOLADA = _PassageType.make_unsided(
        desc = Substantive.make_female('porta fechada com tijolos'),
        flavor_list = (
            _NULL_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA #TODO
        )
_PORTA_TABOAS = _PassageType.make_unsided(
        desc = Substantive.make_female('porta fechada com tábuas'),
        flavor_list = (
            _NULL_ITEM_FLAVOR,
            ),
        key_type=_CHAVE_BASICA #TODO
        )


################################################################################


_POLTRONA = _DecorationItemType(
        Substantive.make_female('poltrona'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _FABRIC_ITEM_FLAVOR,)
        )
_SOFA = _DecorationItemType(
        Substantive.make_male('sofa'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _FABRIC_ITEM_FLAVOR,)
        )
_CADEIRA = _DecorationItemType(
        Substantive.make_female('cadeira'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_MESA = _DecorationItemType(
        Substantive.make_female('mesa'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_MESA_DE_CENTRO = _DecorationItemType(
        Substantive.make_female('mesa de centro'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_MESA_DE_CABECEIRA = _DecorationItemType(
        Substantive.make_female('mesa de cabeceira'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_PIA = _DecorationItemType(
        Substantive.make_female('pia'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,)
        )
_LAREIRA = _DecorationItemType(
        Substantive.make_female('lareira'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,)
        )
_FOGAO = _DecorationItemType(
        Substantive.make_male('fogão'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,)
        )
_CAMA = _DecorationItemType(
        Substantive.make_female('cama'),
        (
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _FABRIC_ITEM_FLAVOR,)
        )
_ESTANTE = _DecorationItemType(
        Substantive.make_female('estante'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_ESTANTE_DE_LIVROS = _DecorationItemType(
        Substantive.make_female('estante de livros'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_ARMARIO = _DecorationItemType(
        Substantive.make_male('armário'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_CRISTALEIRA = _DecorationItemType(
        Substantive.make_female('cristaleira'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,)
        )
_ESPELHO = _DecorationItemType(
        Substantive.make_male('espelho'),
        (
            _BASE_ITEM_FLAVOR,)
        )
_QUADRO = _DecorationItemType(
        Substantive.make_male('quadro'),
        (
            _BASE_ITEM_FLAVOR,
            _WOODEN_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,)
        )
_TAPETE = _DecorationItemType(
        Substantive.make_male('tapete'),
        (
            _BASE_ITEM_FLAVOR,
            _USEBLAE_ITEM_FLAVOR,
            _FABRIC_ITEM_FLAVOR,)
        )
_BUSTO = _DecorationItemType(
        Substantive.make_male('busto'),
        (
            _BASE_ITEM_FLAVOR,
            _ART_ITEM_FLAVOR,)
        )
_LUSTRE = _DecorationItemType(
        Substantive.make_male('lustre'),
        (
            _BASE_ITEM_FLAVOR,)
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
            (None, _CRISTALEIRA, _ESTANTE, _ESTANTE_DE_LIVROS, _ARMARIO,),
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
            (None, _CRISTALEIRA, _ARMARIO, _ESTANTE, _ESTANTE_DE_LIVROS,),
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
            (None, _ARMARIO, _ESTANTE, _ESTANTE_DE_LIVROS,),
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
            (_ESTANTE_DE_LIVROS,),
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
        )
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
        repeat = True)
_DEPOSITO = _PlaceType(
        Substantive.make_male('Depósito'),
        (
            (None, _ESTANTE,),
            (None, _ARMARIO,)
            ),
        repeat = True)
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
            ))
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
            ))
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
                ),
            (
                _ESCADA,
                _PASSAGEM,
                _PASSAGEM_ADORNADA,
                _PORTA,
                _PORTA_DUPLA,
                _PORTA_ADORNADA,
                _PASSAGEM_SECRETA_LIVROS,
                _PASSAGEM_SECRETA_QUADRO,
                _PORTA_TIJOLADA,
                _PORTA_TABOAS,
                ),
        )



