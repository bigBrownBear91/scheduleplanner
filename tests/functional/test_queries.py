import pytest

from myapp.queries import query_leagues, query_teams


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


def test_query_leagues_id_not_in_db(init_database):
    with pytest.raises(ValueError):
        query_leagues(league_id=5)


def test_query_teams_id_and_name_both_specified(init_database):
    with pytest.raises(ValueError):
        query_teams(1, 'Bern')
    with pytest.raises(ValueError):
        query_teams(1, 'Bern', True, 2)


def test_query_teams_id_or_name_or_league_and_allteams_specified(init_database):
    with pytest.raises(ValueError):
        query_teams(1, 'Bern', all_entries=True)
    with pytest.raises(ValueError):
        query_teams(1, all_entries=True)
    with pytest.raises(ValueError):
        query_teams(all_entries=True, league_id=1)


def test_query_teams_id_or_name_not_none_or_all_entries_true_and_league_id_given(init_database):
    with pytest.raises(ValueError):
        query_teams(1, league_id=1)
    with pytest.raises(ValueError):
        query_teams(all_entries=True, league_id=1)


def test_query_teams_search_by_id(init_database):
    team = query_teams(1)
    assert team.id == 1
    assert team.name == 'Bern 1'
    assert team.club.name == 'SK Bern'


def test_query_teams_search_by_name(init_database):
    team = query_teams(team_name='Bern 1')
    assert team.id == 1
    assert team.name == 'Bern 1'
    assert team.club.name == 'SK Bern'


def test_query_teams_all_teams(init_database):
    teams = query_teams(all_entries=True)
    assert isinstance(teams, list)
    assert teams[0].id == 1
    assert teams[0].name == 'Bern 1'


def test_query_teams_search_all_of_league(init_database):
    teams = query_teams(league_id=1)
    assert isinstance(teams, list)
    assert teams[0].id == 1
    assert teams[0].name == 'Bern 1'
