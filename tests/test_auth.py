import time


def test_refresh_token(client):
    time.sleep(0.1)
    assert client.token == "new_token"  # Refreshed token
