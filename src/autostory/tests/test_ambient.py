
def is_exception_raised(lamb):
    try:
        lamb()
        return False
    except:
        return True


def test_has_dependencies():
    assert not is_exception_raised(lambda:__import__('tracery'))
    assert not is_exception_raised(lambda:__import__('adventurelib'))
