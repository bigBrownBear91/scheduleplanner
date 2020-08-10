from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        """
        :param name: Name of the club
        """
        self.name = name

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    pool_id = db.Column(db.Integer, db.ForeignKey('pools.id'))
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'), nullable=False)
    club = db.relationship('Club', backref='clubs')
    person = db.relationship('Person', backref='teams')
    pool = db.relationship('Pool', backref='pools')
    league = db.relationship('League', backref='leagues', lazy='joined')

    def __init__(self, name, club, league, person=None, pool=None):
        """
        :param name: Name of the team
        :param club: Club to which the team belongs
        :param league: League to which the team belongs
        :param person: optional - Contact person
        :param pool: optional - Pool in which the club plays
        """
        self.name = name
        self.club = club
        self.league = league
        self.person = person
        self.pool = pool

    def __repr__(self):
        return f'id:{self.id}, name:{self.name}'


class Pool(db.Model):
    __tablename__ = 'pools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=True)

    def __init__(self, name, address=None):
        """
        Instantiate Pool-class. Only the name is mandatory, the address is optional.

        :param name: Name of the pool
        :param address: The address of the pool
        """
        self.name = name
        self.address = address

    def __repr__(self):
        return f'id:{self.id}, name:{self.name}, address:{self.address}'


class GameDate(db.Model):
    __tablename__ = 'gamedates'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True)
    time = db.Column(db.Time, nullable=True)
    pool_id = db.Column(db.Integer, db.ForeignKey('pools.id'), nullable=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    guest_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    home_team = db.relationship('Team', backref=backref('home_teams', cascade="all, delete"), foreign_keys=[home_team_id])
    guest_team = db.relationship('Team', backref=backref('guest_teams', cascade="all, delete"), foreign_keys=[guest_team_id])
    pool = db.relationship('Pool', backref='gamedates')

    def __init__(self, date, time, pool, home_team, guest_team):
        """
        Instantiate Gamedate-Class. Date, time, pool, home_team and guest_team needs are all mandatory.

        :param date: Date of the game
        :param time: Time of the game
        :param pool: Pool in which to play
        :param home_team: Home team
        :param guest_team: Guest team
        """
        self.date = date
        self.time = time
        self.pool = pool
        self.home_team = home_team
        self.guest_team = guest_team

    def is_complete(self):
        """Returns True if every attribute is set."""
        if self.date and self.time and self.pool and self.home_team and self.guest_team:
            return True
        return False

    def __repr__(self):
        return f'id:{self.id}, date:{self.date}, pool:{self.pool.name}, home_team:{self.home_team.name}, guest_team:' \
               f'{self.guest_team.name}'


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'id:{self.id}, name:{self.name}'
