from myapp.queries import query_leagues
from myapp.models import League


# def test_query_leagues_with_id(create_session):
#     league_one = League('NLB')
#     create_session.add(league_one)
#     create_session.commit()
#
#     querried_league = query_leagues(league_id=1)
#     assert querried_league == league_one

def test_random_query(create_session):
    create_session.query(Teams).all()