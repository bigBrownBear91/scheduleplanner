from datetime import date, time

import pytest

from myapp import create_app
from myapp.models import League, Team, Club, GameDate, Pool, db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test_config.py')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client
    ctx.pop()


@pytest.fixture
def init_database():
    app = create_app('test_config.py')
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        league = League('NLB')
        league_a = League('NLA')
        club = Club('SK Bern')
        club2 = Club('Lugano Pallanuoto')
        team = Team('Bern 1', club, league)
        team2 = Team('Bern 2', club, league)
        team3 = Team('Bern 3', club, league)
        team_lug1 = Team('Lugano1', club2, league_a)
        team_lug2 = Team('Lugano2', club2, league_a)
        pool = Pool('KaWeDe')
        secondpool = Pool('Weyerli')
        gamedate1 = GameDate(date(2020, 6, 21), time(18, 00, 00), pool, team, team2)
        gamedate2 = GameDate(date(2020, 6, 25), time(18, 00, 00), pool, team2, team)
        gamedate = GameDate(date(2020, 6, 21), time(18, 00, 00), Pool('SomePool'), Team('Newteam', club, league),
                            Team('Anothernewteam', club, league))
        club_without_team = Club('Club without team')
        db.session.add_all([league, league_a, club, club2, team, team2, team3, team_lug1, team_lug2, pool, secondpool,
                            gamedate, gamedate1, gamedate2, club_without_team])
        db.session.commit()

        yield db
