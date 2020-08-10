from datetime import date, time

import pytest
from sqlalchemy import types

from myapp.models import Club, Team, Person, Pool, GameDate, League
import myapp.database_handlers as db_handlers


@pytest.fixture(scope='module')
def new_club():
    club = Club('SK Bern')
    return club


@pytest.fixture(scope='module')
def new_team_without_person_and_pool(new_club):
    league = League('NLB')
    team = Team('SK Bern 1', new_club, league)
    return team


@pytest.fixture(scope='module')
def new_person():
    person = Person('Danilo Bigovic')
    return person


@pytest.fixture(scope='module')
def new_pool():
    pool = Pool('Ka-We-De', 'Jubilaumsstrasse 29, 3003 Bern')
    return pool


@pytest.fixture(scope='module')
def new_team_with_person_and_pool(new_club, new_person, new_pool):
    league = League('NLB')
    team = Team('SK Bern 1', new_club, league, new_person, new_pool)
    return team


def test_create_club_instance(new_club):
    assert new_club.name == 'SK Bern'


def test_create_team_instance_without_person_and_pool(new_team_without_person_and_pool):
    assert new_team_without_person_and_pool.name == 'SK Bern 1'


def test_create_instance_person(new_person):
    assert new_person.name == 'Danilo Bigovic'


def test_create_instance_pool(new_pool):
    assert isinstance(new_pool, Pool)
    assert new_pool.name == 'Ka-We-De'
    assert new_pool.address == 'Jubilaumsstrasse 29, 3003 Bern'


def test_create_team_instance_with_person_and_pool(new_team_with_person_and_pool):
    assert new_team_with_person_and_pool.name == 'SK Bern 1'
    assert new_team_with_person_and_pool.person.name == 'Danilo Bigovic'
    assert new_team_with_person_and_pool.pool.name == 'Ka-We-De'


def test_create_instance_game_date(new_pool, new_team_with_person_and_pool):
    guest_team = Team('SP Bissone', club=Club('Bissone'), league=League('NLB'))
    game_date = GameDate(date(2020, 6, 21), time(18, 0, 0), new_pool, new_team_with_person_and_pool, guest_team)
    assert isinstance(game_date, GameDate)
    assert isinstance(game_date.date, date)
    assert isinstance(game_date.time, time)
    assert isinstance(game_date.pool, Pool)
    assert isinstance(game_date.guest_team, Team)
    assert isinstance(game_date.home_team.person, Person)
    assert game_date.date == date(2020, 6, 21)
    assert game_date.home_team.person.name == 'Danilo Bigovic'


def test_gamedate_is_complete_True(new_pool):
    hometeam = Team(name='Bern 1', club=Club('SK Bern'), league=League('NLB'))
    guestteam = Team(name='SP Bissone', club=Club('Bissone'), league=League('NLB'))
    game = GameDate(date(2020, 6, 20), time(20, 00, 00), new_pool, hometeam, guestteam)

    assert game.is_complete() is True


def test_gamedate_is_complete_false():
    hometeam = Team(name='Bern 1', club=Club('SK Bern'), league=League('NLB'))
    guestteam = Team(name='SP Bissone', club=Club('Bissone'), league=League('NLB'))
    game = GameDate(date(2020, 6, 4), None, None, hometeam, guestteam)

    assert game.is_complete() is False
