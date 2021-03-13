from . import example_game
from .. import datamodels

def test_base():
    a = example_game.example_a()

    assert isinstance(a, datamodels.Game)
    for amb in a.ambients:
        assert isinstance(amb, datamodels.Ambient)
        for obj in amb.objects:
            assert isinstance(obj, datamodels.Object)
    for pas in a.passages:
        assert isinstance(pas, datamodels.Passage)
        assert isinstance(pas._from, datamodels.Ambient)
        assert isinstance(pas.to, datamodels.Ambient)
