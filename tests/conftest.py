import os

import pytest

from myapp import create_app
from myapp.models import League, db
from db.create_db import create_db, return_path_to_dbfolder_as_string


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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + return_path_to_dbfolder_as_string() + '/testdb.db'
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        league = League('NLB')
        db.session.add(league)
        db.session.commit()

        yield db
        db.drop_all()
