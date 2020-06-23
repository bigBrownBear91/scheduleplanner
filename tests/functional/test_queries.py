import pytest

from myapp.queries import query_leagues
from myapp.models import League


def test_query_leagues_with_id(init_database):
    querried_league = query_leagues(league_id=1)
    assert querried_league.name == 'NLB'


def test_query_leagues_with_name(init_database):
    querried_league = query_leagues(league_name='NLB')
    assert querried_league.name == 'NLB'


def test_query_leagues_no_parameter(init_database):
    with pytest.raises(ValueError):
        query_leagues()


def test_query_leagues_id_and_name_given(init_database):
    with pytest.raises(ValueError):
        query_leagues(league_id=1, league_name='NLB')


def test_query_id_not_in_db(init_database):
    with pytest.raises(ValueError):
        print(query_leagues(all_entries=True))
        query_leagues(league_id=5)
