from datetime import date, time

from myapp.database_handlers import query_teams, insert_gamedate, query_gamedates, query_person, query_leagues, \
    query_clubs
from tests.helpers import is_order_of_strings_in_string_correct


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
    assert b'KaWeDe' in response.data


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


def test_overview_all_teams(test_client, init_database):
    """
    GIVEN a get request for the url /all_teams
    THEN all test teams are listed ordered by club names and teamnames and status code is 200
    """
    response = test_client.get('/all_teams')

    assert response.status_code == 200
    assert b'SK Bern' in response.data
    assert b'Bern 1' and b'Bern 2' and b'Bern 3' in response.data
    assert b'Lugano Pallanuoto' in response.data
    assert b'Lugano1' and b'Lugano1' in response.data
    assert is_order_of_strings_in_string_correct('Lugano Pallanuoto', 'SK Bern', response.data) is True
    assert is_order_of_strings_in_string_correct(b'Bern 1', b'Bern 2', response.data)


def test_overview_all_teams_links_are_working(test_client, init_database):
    """
    GIVEN a get request for the url /all_teams
    THEN links for all test teams to an update page for the teams respectivley club are generated
        AND a button to a page to insert a new team respectivley club are generated
    """
    response = test_client.get('/all_teams')

    assert b'href="/update_team?team_id=1' in response.data
    assert b'href="/update_team?team_id=2' in response.data


def test_update_team_get(test_client, init_database):
    response = test_client.get('/update_team?team_id=1')

    assert response.status_code == 200
    assert b'Bern 1' in response.data


def test_update_team_post(test_client, init_database):
    """
    GIVEN team1 with name: Bern1, league: NLB and no person
    WHEN post to update team to name: nlb_team_of_bern, person: pesche and league: NLA
    THEN correct update and redirect to all teams
    """
    postdata = {'name': 'nlb_team_of_bern', 'person': 'pesche', 'league': 'NLA'}
    response = test_client.post('/update_team?team_id=1', data=postdata)

    result = query_teams(team_id=1)
    assert result.name == 'nlb_team_of_bern'
    assert result.person == query_person('pesche')
    assert result.league == query_leagues(league_id=2)


def test_get_insert_team(test_client):
    response = test_client.get('/add_new_team')

    assert response.status_code == 200


def test_post_insert_team(test_client, init_database):
    postdata = {'name': 'Bern Damen', 'club': 'SK Bern', 'person': 'Alina', 'league': 'NLA'}
    response = test_client.post('/add_new_team', data=postdata)

    result = query_teams(team_name='Bern Damen')
    assert result.club == query_clubs(club_name='SK Bern')
    assert result.person == query_person(person_name='Alina')
    assert result.league == query_leagues(league_name='NLA')
