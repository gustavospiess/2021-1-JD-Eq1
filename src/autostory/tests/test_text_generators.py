from .. import text_generators


def test_monster_names():
    assert text_generators.monster_names is not None
    for name, _ in zip(text_generators.monster_names(), range(30)):
        assert name


def test_intro_letter():
    assert text_generators.intro_letter is not None
    for intro, _ in zip(text_generators.intro_letter(), range(30)):
        assert intro


def test_contextual_norepeat():
    g = text_generators.tracery.Grammar({
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


def test_context_object():
    context = text_generators.Context()
    assert context.place is not None
    assert isinstance(context.place, text_generators.PlaceContext)
