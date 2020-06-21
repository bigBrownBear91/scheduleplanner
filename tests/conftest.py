import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
def create_session():
    db_path = 'sqlite:///' + return_path_to_dbfolder_as_string() + 'testdb.db'
    engine = db.create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()


@pytest.fixture(scope='session')
def app(request):
    return create_app('test_config.py')


@pytest.fixture(scope='session')
def database(app):
    db = SQLAlchemy(app=test_client)
    return db


@pytest.fixture(scope='session')
def _db(database, request):
    return database
