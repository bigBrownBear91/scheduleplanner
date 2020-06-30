def test_get_index(test_client, init_database):
    """
    GIVEN a flask app
    WHEN '/' is requested
    THEN check whether the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Bern 1' in response.data


def test_get_scheduleplanner(test_client, init_database):
    response = test_client.get('/scheduleplanner?schedule_for_team=1')
    assert response.status_code == 200
    assert b'Bern 1' in response.data
    assert b'Bern 2' in response.data
