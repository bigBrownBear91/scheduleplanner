from sqlalchemy.orm.exc import NoResultFound

from myapp import db
from myapp.models import League, Team, GameDate, Pool, Club, Person


def query_leagues(league_id=None, league_name=None, all_entries=False):
    """
    Returns the entry of a league or a list of all leagues, if all_entries is True. If only one shall be returned,
    either the id or the name of the league must be given. If a list of all leagues is required, both the id and the
    name should be left as None.

    :param league_id: Id of the league which should be returned.
    :param league_name: Name of the league which should be returned.
    :param all_entries: True if a list with all leagues should be returned.
    :return: Either the entry of one league or a list with the entries of all leagues.
    """
    if league_id is None and league_name is None and all_entries is False:
        raise ValueError('None parameter is specified, but at least one parameter must be given')
    if league_id is not None and league_name is not None:
        raise ValueError('Only league_id or league_name may be specified, not both')
    if (league_id is not None or league_name is not None) and all_entries is True:
        raise ValueError('If all_entries is True, league_id and league_name may not be specified')

    if league_id is not None:
        league = League.query.get(league_id)
        if not isinstance(league, League):
            raise ValueError(f'Element with id {league_id} is not in database')
    if league_name is not None:
        league = League.query.filter_by(name=league_name).one()
        if not isinstance(league, League):
            raise ValueError(f'Element with name {league_name} is not in database')
    if all_entries is True:
        league = League.query.all()

    return league


def query_teams(team_id=None, team_name=None, all_entries=False, league_id=None):
    """
    Returns either a team selected by the team id or the team name or a list of all teams in the database or all the
    of a league given a league id.

    :param team_id: The id of the team which should be returned
    :param team_name: The name of the team which should be returned
    :param all_entries: True if a list of all teams should be returned, False else
    :param league_id: The id of the league of which the teams should be returned
    :return: Either a single team or a list of teams
    """

    if team_id is not None and team_name is not None:
        raise ValueError('team_id and team_name cannot be both specified')
    if (team_id is not None or team_name is not None or league_id is not None) and all_entries is True:
        raise ValueError('If all entries is true, both the id and the name must be None')
    if (team_id is not None or team_name is not None or all_entries is True) and league_id is not None:
        raise ValueError('If league_id is given, the other parameters must be None or False')
    if team_id is None and team_name is None and all_entries is False and league_id is None:
        raise ValueError('One of The Parameters has to be specified')

    if team_id is not None:
        team = Team.query.get(team_id)
    if team_name is not None:
        team = Team.query.filter_by(name=team_name).one_or_none()
    if all_entries is True:
        team = Team.query.all()
    if league_id is not None:
        team = Team.query.filter_by(league_id=league_id).all()

    return team


def query_gamedates(hometeam, guestteam):
    """
    Returns a the game of the given teams. If the game is not yet in the database, it will be inserted and returned.

    :param hometeam:
    :param guestteam:
    :return: Game of the two selected teams
    """
    if not isinstance(hometeam, Team) or not isinstance(guestteam, Team):
        raise ValueError('Variable hometeam and guestteam must be of type Team')

    result = GameDate.query.filter((GameDate.home_team == hometeam) & (GameDate.guest_team == guestteam)).one_or_none()
    if result is None:
        gamedate = insert_gamedate(hometeam, guestteam)
        return gamedate

    return result


def insert_gamedate(hometeam, guestteam):
    """
    Inserts new gamedate into database and returns the inserted object.

    :param hometeam:
    :param guestteam:
    :return: The insertet gamedate.
    """
    if not isinstance(hometeam, Team) and not isinstance(guestteam, Team):
        raise ValueError('Hometeam and guestteam have to be of type Team')

    gamedate = GameDate(None, None, None, hometeam, guestteam)
    db.session.add(gamedate)
    db.session.commit()
    return gamedate


def update_gamedates(home_team, guest_team, date, time, pool):
    """
    Updates date, time and pool of a given gamedate.

    :param pool:
    :param time:
    :param home_team:
    :param guest_team:
    :param date:
    :return: True if no exception is raised
    """
    if not isinstance(home_team, Team) or not isinstance(guest_team, Team):
        raise TypeError('Parameters home_team and guest_team has to be of type Team')

    updategamedate = query_gamedates(home_team, guest_team)
    updategamedate.date = date
    updategamedate.time = time
    updategamedate.pool = pool
    db.session.commit()

    return True


def query_pools(pool_id=None, pool_name=None, all_entries=False):
    if not pool_id and not pool_name and not all_entries:
        raise ValueError('Either an id or a name must be given or the flag all_entries must be True')
    if pool_id and pool_name or pool_id and all_entries or pool_name and all_entries or pool_id and pool_name and all_entries:
        raise (ValueError('Only one parameter may be specified'))

    if pool_id:
        return Pool.query.get(pool_id)
    if pool_name:
        try:
            return Pool.query.filter_by(name=pool_name).one()
        except NoResultFound:
            raise NoResultFound(f'The pool {pool_name} is not a known pool or there is a typo.')
    if all_entries:
        return Pool.query.all()


def query_clubs(club_id=None, club_name=None, all_entries=False):
    """
    Returns either one club or all clubs as dictonnaries with the teams belonging to a club as additional attribute. De-
    pending of the chosen parameters only one club is returned or all of them.

    :param club_id:
    :param club_name:
    :param all_entries:
    :return: Either a dict of a club and its teams or a list of dicts for all clubs.
    """

    if club_id is not None and club_name is not None:
        raise ValueError('club_id and club_name cannot be both specified')
    if (club_id is not None or club_name is not None) and all_entries is True:
        raise ValueError('If all entries is true, both the id and the name must be None')
    if club_id is None and club_name is None and all_entries is False:
        raise ValueError('One of The Parameters has to be specified')

    if club_id:
        club = Club.query.get(club_id)
        teams = Team.query.filter_by(club=club).order_by(Team.name).all()
        club.__setattr__('teams', teams)
        return club

    elif club_name:
        try:
            club = Club.query.filter_by(name=club_name).one()
        except NoResultFound:
            raise NoResultFound(f'The club {club_name} is not known or there is a typo in the club name')

        teams = Team.query.filter_by(club=club).order_by(Team.name).all()
        club.__setattr__('teams', teams)
        return club

    elif all_entries:
        clubs = Club.query.order_by(Club.name).all()
        for club in clubs:
            teams = Team.query.filter_by(club=club).order_by(Team.name).all()
            club.__setattr__('teams', teams)

        return clubs

    else:
        raise Exception('There seems to be an error since no option is selected!')


def update_team_instance(team_id, **kwargs):
    """
    Updates the team with the given id with the values passed with kwargs.

    :param team_id: Id of the team to be updated
    :param kwargs: Must be in set (name, person, pool and league).
    :return: Nothing
    """
    team = query_teams(team_id=team_id)

    if not set(kwargs).issubset({'name', 'person', 'pool', 'league'}):
        raise TypeError('The keys for kwargs must be of the set (name, person, pool and league)')

    if kwargs.get('name'): team.name = kwargs.get('name')
    if kwargs.get('person'): team.person = query_person(kwargs.get('person'))
    if kwargs.get('pool'): team.pool = query_pools(pool_name=kwargs.get('pool'))
    if kwargs.get('league'): team.league = query_leagues(league_name=kwargs.get('league'))

    db.session.commit()


def query_person(person_name):
    """
    Returns the person. If this person doesn't exist yet, it is created and returned.

    :param person_name: Name of the person.
    :return: Instance of the person.
    """
    result = Person.query.filter_by(name=person_name).one_or_none()

    if not result:
        newperson = Person(person_name)
        db.session.add(newperson)
        db.session.commit()
        result = query_person(newperson.name)

    return result


def insert_team(**kwargs):
    if not kwargs.get('name'):
        raise TypeError('A team name must be specified')
    if not kwargs.get('league'):
        raise TypeError('Every team needs to play in a league')
    if not kwargs.get('club'):
        raise TypeError('Every team has to belong to a club')
    if query_teams(team_name=kwargs.get('name')):
        raise ValueError(f'A team with the name {kwargs["name"]} exists already. Choose another name!')

    newteam = Team(kwargs['name'],
                   query_clubs(club_name=kwargs.get('club')),
                   query_leagues(league_name=kwargs.get('league')))
    with db.session.no_autoflush:
        if kwargs.get('pool'): newteam.pool = query_pools(pool_name=kwargs.get('pool'))
        if kwargs.get('person'): newteam.person = query_person(kwargs.get('person'))

    db.session.add(newteam)
    db.session.commit()
