import tracery

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


class SuperContext():
    def __init__(self):
        print(self)
        pass


class Context(SuperContext):
    def __init__(self):
        super().__init__();
        self.place = PlaceContext()


class PlaceContext(SuperContext):
    def __init__(self):
        super().__init__();
        pass