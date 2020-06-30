#!/usr/bin/env python3.7
"""
This scripts contains a method to create an sqlite database file and a method to populate a database with basic data
from a sql-script. If the module is run directly, a development database is created and populated.
"""
import os
import sqlite3

from myapp import create_app
from myapp.models import db

db_file_name = {'development': 'devdb.db', 'testing': 'testdb.db'}


def create_db(system, config):
    """
    Creates a sqlite database file. If there's already an existing db, this db will be removed first.

    :param system: Development or testing system. Allowed values: 'development' or 'testing'
    :param config: Config file with which the database should be created.
    :return: None
    """
    if system not in db_file_name:
        raise ValueError(f'Parameter {system} is not in {db_file_name.values()}')

    if os.path.isfile(db_file_name[system]):
        os.remove(db_file_name[system])

    db_file = open(db_file_name[system], 'w+')
    db_file.close()

    populate_db(config, system)


def populate_db(config, system):
    """
    Creates all tables in a database file and populates said tables.

    :param config: Config-file to be used
    :param system: Development or testing system. Allowed values: 'development' or 'testing'
    :return: The db-instance
    """
    path = os.path.abspath(os.path.dirname(__file__))

    app = create_app(config)
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///' + path + '/' + db_file_name[system])
    db.create_all(app=app)

    if system != 'testing':
        basic_data_script = open(path + '/' + 'basic_data.sql').read()

        with sqlite3.connect(db_file_name[system]) as conn:
            cursor = conn.cursor()
            cursor.executescript(basic_data_script)


def return_path_to_dbfolder_as_string():
    path = os.path.abspath(os.path.dirname(__file__))
    return str(path)


if __name__ == '__main__':
    create_db('development', 'dev_config.py')
