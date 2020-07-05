from datetime import date, time
import pytest

from myapp import db
from myapp.database_helpers import query_leagues, query_teams, query_gamedates, insert_gamedate
from myapp.models import GameDate, Team, Club, League


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


def test_query_teams_no_parameter_specified(init_database):
    with pytest.raises(ValueError):
        query_teams()
    with pytest.raises(ValueError):
        query_teams(None, None, False, None)


def test_query_gamedates_if_games_in_db(init_database):
    hometeam = query_teams(team_id=1)
    guestteam = query_teams(team_id=2)
    result = query_gamedates(hometeam, guestteam)

    assert isinstance(result, GameDate)
    assert result.date == date(2020, 6, 21)
    assert result.time == time(18, 00, 00)
    assert result.pool.name == 'KaWeDe'
    assert result.home_team == hometeam
    assert result.guest_team == query_teams(team_id=2)


def test_insert_gamedate(init_database):
    newclub = Club('Newclub')
    league = League('Newleague')
    newteam1 = Team('newteam1', newclub, league)
    newteam2 = Team('newteam2', newclub, league)
    db.session.add_all([newclub, league, newteam1, newteam2])
    db.session.commit()
    insert_gamedate(newteam1, newteam2)
    result = GameDate.query.get(4)

    assert result.home_team == newteam1
    assert result.guest_team == newteam2


def test_insert_gamedate_parameters_not_teams(init_database):
    with pytest.raises(ValueError):
        insert_gamedate('string', 3)
