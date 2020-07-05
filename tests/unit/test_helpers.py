from myapp.helpers import ValuesQuerystring


def test_valueQueryStringInts():
    url = 'http://www.scheduleplanner?id=1&otherid=2'
    vqs = ValuesQuerystring(url)
    assert vqs.id == 1
    assert vqs.otherid == 2


def test_valueQueryStringStrings():
    url = 'http://www.scheduleplaner?id=1&otherteam=team'
    vqs = ValuesQuerystring(url)
    assert vqs.id == 1
    assert vqs.otherteam == 'team'
