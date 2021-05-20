from .. import text_generators


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

    a = text_generators.Adjective.make_format(lambda g: f'{g}')
    assert a.m  == 'o'
    assert a.ms == 'os'
    assert a.f  == 'a'
    assert a.fs == 'as'


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
