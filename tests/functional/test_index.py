def test_get_index(test_client, init_database):
    """
    GIVEN a flask app
    WHEN '/' is requested
    THEN check whether the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
