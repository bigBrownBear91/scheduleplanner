from datetime import date, time
import mock

from myapp.helpers import ValuesQuerystring, StringToDate, StringToTime, RepresentationGame
from myapp.database_handlers import query_gamedates
import myapp.models as models


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


def test_stringToDateValidInput():
    testdate = date(2020, 2, 12)

    assert StringToDate('12.02.2020').date_as_date == testdate
    assert StringToDate('12.2.2020').date_as_date == testdate
    assert StringToDate('12.2.20').date_as_date == testdate
    assert StringToDate('12.02.20').date_as_date == testdate


def test_stringToTimeValidInput():
    assert StringToTime('18.30').time_as_time == time(18, 30, 00)
