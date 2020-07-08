from datetime import date, time

from myapp import db
from myapp.database_handlers import query_teams, insert_gamedate, query_gamedates
from myapp.models import GameDate, Team


def test_get_index(test_client, init_database):
    """
    GIVEN a flask app
    WHEN '/' is requested
    THEN check whether the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Bern 1' in response.data


def test_get_scheduleplanner_all_teams(test_client, init_database):
    response = test_client.get('/scheduleplanner?schedule_for_team=1')
    assert response.status_code == 200
    assert b'Bern 1' in response.data
    assert b'Bern 2' in response.data


def test_get_scheduleplanner_gamedate_of_one_team(test_client, init_database):
    response = test_client.get('/scheduleplanner?schedule_for_team=1&second_team_id=2')
    assert response.status_code == 200
    assert b'Bern 1' in response.data
    assert b'Bern 2' in response.data


def test_update_gamedates_from_scheduleplanner(test_client, init_database):
    """
    GIVEN a form with updates for a home and away game
    WHEN a post request for the url /scheduleplanner is made
    THEN updates the gamedates of the given games and redirects to all games of the schedule-for team
    """
    team1 = query_teams(team_name='Bern 1')
    team2 = query_teams(team_name='Bern 3')

    insert_gamedate(team1, team2)
    insert_gamedate(team2, team1)

    postdata = {'home_hometeam': 'Bern 1', 'home_guestteam': 'Bern 3', 'home_date': '25.6.2020',
                'home_time': '18.00', 'home_pool': 'KaWeDe', 'guest_hometeam': 'Bern 3',
                'guest_guestteam': 'Bern 1', 'guest_date': '21.03.2020', 'guest_time': '18.30',
                'guest_pool': 'Weyerli'}
    response = test_client.post('/scheduleplanner', data=postdata)

    game1 = query_gamedates(team1, team2)
    game2 = query_gamedates(team2, team1)

    assert game1.date is not None
    assert game1.date == date(2020, 6, 25)
    assert game1.time is not None
    assert game1.time == time(18, 00, 00)
    assert game1.pool is not None
    assert game1.home_team == query_teams(team_name='Bern 1')
    assert game1.guest_team == query_teams(team_name='Bern 3')

    assert game2.date is not None
    assert game2.date == date(2020, 3, 21)
    assert game2.time is not None
    assert game2.time == time(18, 30, 00)
    assert game2.pool is not None
    assert game2.home_team == query_teams(team_name='Bern 3')
    assert game2.guest_team == query_teams(team_name='Bern 1')

    assert response.status_code == 302
