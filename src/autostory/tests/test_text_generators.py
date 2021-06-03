from .. import text_generators
from collections import Counter
from pprint import pp


def test_monster_names():
    assert text_generators.monster_names is not None
    for name, _ in zip(text_generators.monster_names(), range(30)):
        assert name


def test_intro_letter():
    assert text_generators.intro_letter is not None
    for intro, _ in zip(text_generators.intro_letter(), range(30)):
        assert intro


def test_location_names():
    assert text_generators.location_names is not None
    for name, _ in zip(text_generators.location_names(), range(30)):
        assert name


def test_contextual_norepeat():
    g = text_generators.Grammar({
        'a': [str(i) for i in range(50)],
        'b': 'lorem',
        'empty': ''
        })
    mod = text_generators.Context().make_modifires(g)
    g.add_modifiers(mod)
    for i in range(50):
        assert len({g.flatten('#empty.norepeat(a)#') for _ in range(49)}) == 49
        assert g.flatten('#empty.norepeat#') == g.flatten('#empty#')
        assert g.flatten('#lorem.norepeat#') == g.flatten('#lorem#')
        mod.reset_norepeat()


def test_contextual_norepeat_sparce():
    g = text_generators.Grammar({
        'a': ['a'],
        'b': ['a', 'b'],
        'empty': ''
        })
    mod = text_generators.Context().make_modifires(g)
    g.add_modifiers(mod)
    for i in range(50):
        g.flatten('#empty.norepeat(a)#')
        assert g.flatten('#empty.norepeat(b)#') == 'b'
        mod.reset_norepeat()

    g = text_generators.Grammar({
        'a': ['a'],
        'b': ['a'],
        'empty': ''
        })
    mod = text_generators.Context().make_modifires(g)
    g.add_modifiers(mod)
    for i in range(50):
        g.flatten('#empty.norepeat(a)#')
        assert g.flatten('#empty.norepeat(b)#') == 'a'
        mod.reset_norepeat()


def test_contextual_norepeat_inirect():
    g = text_generators.Grammar({
        'a': ['b'],
        'b': ['lorem'],
        'empty': ''
        })
    mod = text_generators.Context().make_modifires(g)
    g.add_modifiers(mod)
    assert g.flatten('#empty.norepeat(a)#') == 'lorem'



def test_contextual_gender():
    g = text_generators.Grammar({
        'female': 'a',
        'male': 'o',
        'bonito_a': 'bonita',
        'bonito_o': 'bonito',
        })
    mod = text_generators.Context().make_modifires(g)
    g.add_modifiers(mod)
    assert g.flatten('#female.gender(bonito)#') == 'bonita'
    assert g.flatten('#male.gender(bonito)#') == 'bonito'

def test_context_object():
    for _ in range(10):
        context = text_generators.Context()
        assert context.map is not None
        g = context.map.grammar
        assert g.flatten('#adjetivo#')
        assert g.flatten('#nome#')
        assert g.flatten('#tipo#')


def test_map_generation():
    for _ in range(10):
        context = text_generators.Context()
        desc = context.map.describe
        assert desc


def test_place_generation():
    context = text_generators.Context()
    for _ in range(50):
        place = context.make_place()
        desc = place.describe()
        assert desc
        if len(place.decorations) > 1:
            assert ' e ' in desc
            for deco in place.decorations:
                assert deco.desc.word in desc


def test_place_generation_no_repeat():
    context = text_generators.Context()
    type_counter = Counter()
    for _ in range(50):
        place = context.make_place()
        type_counter[place.place_type] += 1

    for place_type, qtd in type_counter.items():
        assert place_type.repeat or qtd == 1

    
def test_passage_generation():
    builder = text_generators.MapBuilder()
    for i in range(50):
        builder.create_passage(i, i+1, False)
        passage_a = builder.passage_map[i][i+1]
        passage_b = builder.passage_map[i+1][i]
        desc = passage_a.describe()
        assert desc
        desc = passage_b.describe()
        assert desc


def test_passage_distribution():
    builder = text_generators.MapBuilder()
    builder.create_passage(0, 1, False)
    builder.create_ambient(0)
    builder.create_ambient(1)
    for place in builder.ambient_list:
        assert place.passages[0].nome.word in place.describe()
        assert place.passages[0].locked == False
    builder = text_generators.MapBuilder()
    builder.create_passage(0, 1, True)
    builder.create_ambient(0)
    builder.create_ambient(1)
    for place in builder.ambient_list:
        assert place.passages[0].nome.word in place.describe()
        assert place.passages[0].locked == True


def test_passage_distribution():
    builder = text_generators.MapBuilder()
    builder.create_passage(0, 1, False)
    builder.create_passage(0, 2, True)
    builder.create_ambient(0)
    builder.create_ambient(1)
    builder.create_ambient(2)
    b = builder.build()

    pp(b.as_dict())
    dct = b.as_dict()
    for amb in dct['ambients']:
        for pas in amb['passages']:
            assert pas in map(lambda p: p['descritption'], dct['passages'])

    assert 0
