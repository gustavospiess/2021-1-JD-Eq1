
_MONSTER_NAME = {
        'main' : ['#part#'*i for i in range(2,5)],
        'part': ['#sub_a#', '#sub_b##sub_a#'],
        'sub_a': '#a_vog##a_con#',
        'a_vog': ['a', 'e', 'i', 'o', 'u'],
        'a_con': ['l', 'z', 'k', 'w', 'm', 'n'],
        'sub_b': ['ch', 'x', 'k', 'd', 'm', 't', 'tr', 'th'],
        }


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


_MAP_BASE_DESCRIPTION ='''
    #tipo_o# #tipo# #nome# é um lugar #empty.norepeat(adjetivo_o)# com seus muros
    #empty.norepeat(adjetivo_os)# e seus portais #empty.norepeat(adjetivo_os)#. As
    paredes #empty.norepeat(adjetivo_as)# e #empty.norepeat(adjetivo_as)#, o piso e
    as tábuas #empty.norepeat(adjetivo_as)#, os móveis
    #empty.norepeat(adjetivo_os)#. Tudo parece causar um medo primitivo, como se a
    sua alma estivesse se tornando #empty.norepeat(adjetivo_a)# conforme você olha
    para esta silhueta #empty.norepeat(adjetivo_a)#. Este não é o local onde você
    queria estar.'''


_PLACE_BASE_DESCRIPTION = [
        '''[temp:adjetivo_#tipo_o#] [temp2:adjetivo_comp_#tipo_o#] #tipo_um# #tipo# #empty.norepeat(temp)# e #empty.norepeat(temp2)#. ''', 
        '''[temp:adjetivo_#tipo_o#] #tipo_um# #tipo# #empty.norepeat(temp)#. ''',
        '''[temp2:adjetivo_comp_#tipo_o#] #tipo_um# #tipo# #empty.norepeat(temp)# #empty.norepeat(temp2)#.''']


_PASSAGE_BASE_DESCRIPTION = '''[temp:adjetivo_#nome_o#] #nome_um# #nome# #empty.norepeat(temp)#'''


