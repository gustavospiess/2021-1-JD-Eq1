from typing import NamedTuple

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


