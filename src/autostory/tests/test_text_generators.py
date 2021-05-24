from .. import text_generators


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
    mod = text_generators.ContextualModifiers(g, text_generators.Context())
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
    mod = text_generators.ContextualModifiers(g, text_generators.Context())
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
    mod = text_generators.ContextualModifiers(g, text_generators.Context())
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
    mod = text_generators.ContextualModifiers(g, text_generators.Context())
    g.add_modifiers(mod)
    assert g.flatten('#empty.norepeat(a)#') == 'lorem'



def test_contextual_gender():
    g = text_generators.Grammar({
        'female': 'a',
        'male': 'o',
        'bonito_a': 'bonita',
        'bonito_o': 'bonito',
        })
    mod = text_generators.ContextualModifiers(g, text_generators.Context())
    g.add_modifiers(mod)
    assert g.flatten('#female.gender(bonito)#') == 'bonita'
    assert g.flatten('#male.gender(bonito)#') == 'bonito'

def test_context_object():
    for _ in range(10):
        context = text_generators.Context()
        assert context.map is not None
        g = text_generators.make_grammar(context.map)
        assert g.flatten('#adjetivo#')
        assert g.flatten('#nome#')
        assert g.flatten('#tipo#')


def test_map_generation():
    for _ in range(10):
        context = text_generators.Context()
        desc = text_generators.describe(context.map)
        assert desc


def test_place_generation():
    context = text_generators.Context()
    for _ in range(20):
        place = context.map.make_place()
        desc = text_generators.describe(place)
        assert desc
        if len(place.decorations) > 1:
            assert ' e ' in desc
            for deco in place.decorations:
                assert deco.desc.word in desc
