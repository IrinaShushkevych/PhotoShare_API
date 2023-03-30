from src.config.settings import messages


def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': messages.app_welcome}


def test_healthchecker(client):
    response = client.get('/healthchecker')
    assert response.status_code == 200
    assert response.json() == {'message': messages.app_welcome}

