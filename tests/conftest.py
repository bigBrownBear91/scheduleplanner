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


@pytest.fixture(scope='module')
def init_database():
    app = create_app('test_config.py')
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        league = League('NLB')
        club = Club('SK Bern')
        team = Team('Bern 1', club, league)
        team2 = Team('Bern 2', club, league)
        pool = Pool('KaWeDe')
        gamedate1 = GameDate(date(2020, 6, 21), time(18, 00, 00), pool, team, team2)
        gamedate2 = GameDate(date(2020, 6, 25), time(18, 00, 00), pool, team2, team)
        gamedate = GameDate(date(2020, 6, 21), time(18, 00, 00), Pool('SomePool'), Team('Newteam', club, league),
                            Team('Anothernewteam', club, league))
        db.session.add_all([league, club, team, team2, pool, gamedate, gamedate1, gamedate2])
        db.session.commit()

        yield db
        db.drop_all()
