from datetime import date, time
import pytest

from sqlalchemy.orm.exc import NoResultFound

from myapp import db
from myapp.database_handlers import query_leagues, query_teams, query_gamedates, insert_gamedate, update_gamedates, \
    query_pools, query_clubs, update_team_instance, query_person, insert_team
from myapp.models import GameDate, Team, Club, League, Pool, Person


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


def test_query_leagues_all_entries(init_database):
    result = query_leagues(all_entries=True)

    assert result == [League.query.get(1), League.query.get(2)]


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
    assert teams == Team.query.all()


def test_query_teams_search_all_of_league_leagueid_2(init_database):
    teams = query_teams(league_id=2)

    assert isinstance(teams, list)
    assert teams[0].name == 'Lugano1'
    assert teams[1].name == 'Lugano2'
    assert set(teams) == {Team.query.get(6), Team.query.get(7)}


def test_query_team_search_leagueid_1(init_database):
    nlb_teams = query_teams(league_id=1)

    assert set(nlb_teams) == {query_teams(team_name='Bern 1'), query_teams(team_name='Bern 2'), query_teams(team_name='Bern 3'),
                     query_teams(team_name='Newteam'), query_teams(team_name='Anothernewteam')}


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


def test_query_gamedates_game_not_in_db(init_database):
    hometeam = query_teams(team_id=1)
    guestteam = query_teams(team_id=3)
    result = query_gamedates(hometeam, guestteam)

    assert result.home_team == hometeam
    assert result.guest_team == guestteam


def test_insert_gamedate(init_database):
    newclub = Club('Newclub')
    league = League('Newleague')
    newteam1 = Team('newteam1', newclub, league)
    newteam2 = Team('newteam2', newclub, league)
    db.session.add_all([newclub, league, newteam1, newteam2])
    db.session.commit()
    insert_gamedate(newteam1, newteam2)
    result = query_gamedates(newteam1, newteam2)

    assert result.home_team == newteam1
    assert result.guest_team == newteam2


def test_insert_gamedate_parameters_not_teams(init_database):
    with pytest.raises(ValueError):
        insert_gamedate('string', 3)


def test_update_gamedate(init_database):
    home_team = query_teams(team_id=1)
    guest_team = query_teams(team_id=2)
    pool = query_pools(pool_name='Weyerli')

    update_gamedates(home_team, guest_team, date(2020, 7, 1), time(18, 00, 00), pool)
    test_result = query_gamedates(home_team, guest_team)

    assert test_result.home_team == home_team
    assert test_result.guest_team == guest_team
    assert test_result.date == date(2020, 7, 1)
    assert test_result, time == time(18, 00, 00)
    assert test_result.pool == db.session.query(Pool).filter_by(name='Weyerli').one()


def test_query_pool_by_id_if_existing(init_database):
    result = query_pools(pool_id=1)

    assert result.id == 1
    assert result.name == 'KaWeDe'


def test_query_pool_by_name(init_database):
    result = query_pools(pool_name='KaWeDe')

    assert result.id == 1
    assert result.name == 'KaWeDe'


def test_query_pool_all_entries(init_database):
    result = query_pools(all_entries=True)

    assert len(result) == 3


def test_query_pool_no_parameter_given(init_database):
    with pytest.raises(ValueError):
        query_pools()


def test_query_pool_more_than_one_parameter(init_database):
    with pytest.raises(ValueError):
        query_pools(pool_id=1, pool_name='KaWeDe')
    with pytest.raises(ValueError):
        query_pools(pool_name='Weyerli', all_entries=True)


def test_query_pool_unknown_pool_name(init_database):
    with pytest.raises(NoResultFound):
        query_pools(pool_name='UnknownPool')


def test_query_clubs_by_id(init_database):
    result = query_clubs(club_id=1)

    assert result.id == 1
    assert result.name == 'SK Bern'
    assert len(result.teams) == 5  # Newteam and Anothernewteam made for gamedates are also in the database, therefore 5
    assert isinstance(result.teams[0], Team)
    assert result.teams[0].name == 'Anothernewteam'
    assert result.teams[1].name == 'Bern 1'
    assert result.teams[2].name == 'Bern 2'


def test_query_clubs_by_name(init_database):
    result = query_clubs(club_name='SK Bern')

    assert result.id == 1
    assert result.name == 'SK Bern'
    assert len(result.teams) == 5
    assert isinstance(result.teams[0], Team)
    assert result.teams[0].name == 'Anothernewteam'
    assert result.teams[1].name == 'Bern 1'
    assert result.teams[2].name == 'Bern 2'


def test_query_clubs_all(init_database):
    result = query_clubs(all_entries=True)

    assert len(result) == 3
    assert result[0].name == 'Club without team'
    assert result[1].name == 'Lugano Pallanuoto'
    assert result[2].name == 'SK Bern'


def test_query_clubs_no_parameter_given(init_database):
    with pytest.raises(ValueError):
        query_clubs()


def test_query_clubs_more_than_one_parameter(init_database):
    with pytest.raises(ValueError):
        query_clubs(club_id=1, club_name='SK Bern')
    with pytest.raises(ValueError):
        query_clubs(club_name='SK Bern', all_entries=True)


def test_query_club_unknown_club_name(init_database):
    with pytest.raises(NoResultFound):
        query_clubs(club_name='UnknownPool')


def test_update_team_everything_nullable_is_null(init_database):
    """
    GIVEN team 1 with only name and league specified
    WHEN an update for name = updatedteamname, person = momcilo, pool = Weyerli and league = nla is made
    THEN the attributes are stored into the db
    """
    update_team_instance(team_id=1, **{'name': 'updatedteamname', 'person': 'momcilo', 'pool': 'Weyerli', 'league': 'NLA'})
    result = query_teams(team_id=1)

    assert result.name == 'updatedteamname'
    assert isinstance(result.person, Person) == isinstance(query_person('momcilo'), Person)
    assert result.person == query_person('momcilo')
    assert result.pool == query_pools(pool_name='Weyerli')
    assert result.league == query_leagues(league_name='NLA')


def test_update_team_only_pool(init_database):
    """
    GIVEN a team with its name and person specified
    WHEN only the pool is updated
    THEN leaves the other attributes unchanged
    """
    newteam = Team('testupdateteam', club=query_clubs(club_id=2), person=Person('testupdateperson'),
                   league=query_leagues(league_name='NLA'))
    db.session.add(newteam)
    db.session.commit()

    team = query_teams(team_name='testupdateteam')
    update_team_instance(team.id, **{'pool': 'Weyerli'})

    assertteam = query_teams(team_name='testupdateteam')
    assert assertteam.name == 'testupdateteam'
    assert assertteam.person == query_person('testupdateperson')
    assert assertteam.pool.name == 'Weyerli'
    assert assertteam.league == query_leagues(league_name='NLA')


def test_insert_team_name_club_league_given(init_database):
    insert_team(**{'name': 'Bern 10', 'league': 'NLB', 'club': 'SK Bern'})
    result = query_teams(team_name='Bern 10')

    assert result.name == 'Bern 10'
    assert result.league == query_leagues(league_name='NLB')
    assert result.club == query_clubs(club_name='SK Bern')


def test_insert_team_name_person_pool_club_league_given(init_database):
    insert_team(**{'name': 'Bern 11', 'person': 'Momcilo', 'pool': 'Weyerli', 'league': 'NLB', 'club': 'SK Bern'})
    result = query_teams(team_name='Bern 11')

    assert result.name == 'Bern 11'
    assert result.league == query_leagues(league_name='NLB')
    assert result.person == query_person(person_name='Momcilo')
    assert result.club == query_clubs(club_name='SK Bern')


def test_insert_team_exception_no_name(init_database):
    with pytest.raises(TypeError):
        insert_team(**{'person': 'Pesche', 'pool': 'Weyerli', 'league': 'NLB', 'club': 'SK Bern'})


def test_insert_team_exception_league_and_club(init_database):
    with pytest.raises(TypeError):
        insert_team(**{'name': 'Bern 10', 'person': 'Pesche'})


def test_insert_team_teamname_already_given(init_database):
    with pytest.raises(ValueError):
        insert_team(**{'name': 'Bern 1', 'club': 'SK Bern', 'league': 'NLB'})
