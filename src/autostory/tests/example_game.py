from .. import datamodels

def example_a():
    table = datamodels.Object('Mesa', 'Uma mesa de madeira com marcas de uso. Ela parece um pouco velha, e com um olhar mais atento é possível perceber algumas ranhuras feitas com faca.')
    chair = datamodels.Object('Cadeira', 'Uma cadeira de madeira um pouco velha, ela é um pouco bamba, um dos pés parece ser mais curto que o outro.')
    paint = datamodels.Object('Pintura', 'Uma pintura macabra de um fazendeiro matando um bezerro, feita com óleo')
    key = datamodels.Item('Chave', 'Uma pequena chave de metal enferrujado encontrada sobre a mesa.')

    room_a = datamodels.Ambient([table, chair, paint, key])

    suicide_note = datamodels.Item('Manoescrito', 'Uma página de caderno escrita a mão com os dizeres: Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
    corpse = datamodels.Object('Cadável', 'Um cadáver de um homem branco de cinquenta anos, encontrado com a arma ainda presa em suas mãos, o revolver abriu a parte de trás da cabeça dele, deixando o tecido cerebral exposto.')
    gun = datamodels.Item('Revolver', 'Um revolver antigo, galibre 22, encontrado junto ao corpo do antigo dono')

    room_b = datamodels.Ambient([suicide_note, corpse, gun])

    passage_ab = datamodels.Passage(room_a, room_b, 'Porta', 'Uma porta de madeira velha, com a tinta branca descolando')

    room_a.objects.append(passage_ab)
    room_b.objects.append(passage_ab)

    game = datamodels.Game([room_a, room_b], [passage_ab])

    return game
