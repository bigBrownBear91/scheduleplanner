from myapp.models import League


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
