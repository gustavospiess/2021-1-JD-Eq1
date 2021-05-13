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
    mod = text_generators.ContextualModifiers(g)
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
    mod = text_generators.ContextualModifiers(g)
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
    mod = text_generators.ContextualModifiers(g)
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
    mod = text_generators.ContextualModifiers(g)
    g.add_modifiers(mod)
    assert g.flatten('#empty.norepeat(a)#') == 'lorem'



def test_contextual_gender():
    g = text_generators.Grammar({
        'female': 'a',
        'male': 'o',
        'bonito_a': 'bonita',
        'bonito_o': 'bonito',
        })
    mod = text_generators.ContextualModifiers(g)
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


def test_map_generation_1():
    for _ in range(10):
        context = text_generators.Context()
        d = text_generators.describe(context.map)
        assert d


def test_place_generation():
    context = text_generators.Context()
    for _ in range(20):
        place = context.map.make_place()
        d = text_generators.describe(place)
        assert d


def test_adjective_data_class():
    a = text_generators.Adjective('male', 'males', 'female', 'females')
    assert a.m  == 'male'
    assert a.ms == 'males'
    assert a.f  == 'female'
    assert a.fs == 'females'

    a = text_generators.Adjective(ms='male', m='males', fs='female', f='females')
    assert a.ms == 'male'
    assert a.m  == 'males'
    assert a.fs == 'female'
    assert a.f  == 'females'

    a = text_generators.Adjective.make('radical_')
    assert a.m  == 'radical_o'
    assert a.ms == 'radical_os'
    assert a.f  == 'radical_a'
    assert a.fs == 'radical_as'

    a = text_generators.Adjective.make('radical_')
    assert a.m  == 'radical_o'
    assert a.ms == 'radical_os'
    assert a.f  == 'radical_a'
    assert a.fs == 'radical_as'

    a = text_generators.Adjective.make('radical', ms='male', m='males', fs='female', f='females')
    assert a.ms == 'male'
    assert a.m  == 'males'
    assert a.fs == 'female'
    assert a.f  == 'females'

    a = text_generators.Adjective.make_agender('radical_')
    assert a.m  == 'radical_'
    assert a.ms == 'radical_s'
    assert a.f  == 'radical_'
    assert a.fs == 'radical_s'

    a = text_generators.Adjective.make_agender('radical_', same=True)
    assert a.m  == 'radical_'
    assert a.ms == 'radical_'
    assert a.f  == 'radical_'
    assert a.fs == 'radical_'

    a = text_generators.Adjective.make_agender('radical_', rad_s='radical_s_')
    assert a.m  == 'radical_'
    assert a.ms == 'radical_s_'
    assert a.f  == 'radical_'
    assert a.fs == 'radical_s_'

def test_substantive_data_class():
    s = text_generators.Substantive(1, 2, 3)
    assert s.word == 1
    assert s.o == 2
    assert s.um == 3
    raw = s.raw('pre')
    assert raw['pre'] == 1
    assert raw['pre_o'] == 2
    assert raw['pre_um'] == 3

    s = text_generators.Substantive.make_male(1)
    assert s.word == 1
    assert s.o == 'o'
    assert s.um == 'um'
    raw = s.raw('pre')
    assert raw['pre'] == 1
    assert raw['pre_o'] == 'o'
    assert raw['pre_um'] == 'um'

    s = text_generators.Substantive.make_female(1)
    assert s.word == 1
    assert s.o == 'a'
    assert s.um == 'uma'
    raw = s.raw('pre')
    assert raw['pre'] == 1
    assert raw['pre_o'] == 'a'
    assert raw['pre_um'] == 'uma'
