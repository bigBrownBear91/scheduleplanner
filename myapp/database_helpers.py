from myapp import db
from myapp.models import League, Team, GameDate


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
        team = Team.query.filter_by(name=team_name).one()
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
        insert_gamedate(hometeam, guestteam)

    return result


def insert_gamedate(hometeam, guestteam):
    """
    Inserts new gamedate into database.

    :param hometeam:
    :param guestteam:
    :return: None
    """
    if not isinstance(hometeam, Team) and not isinstance(guestteam, Team):
        raise ValueError('Hometeam and guestteam have to be of type Team')

    gamedate = GameDate(None, None, None, hometeam, guestteam)
    db.session.add(gamedate)
    db.session.commit()


def update_gamedates():
    from time import sleep
    sleep(5)
    return True
