from .. import generate_json
from json import dumps, loads
from pprint import pp


def test_is_json():
    j = generate_json()
    try:
        loads(j)
        assert True
    except:
        assert False
