from vandarpy.endpoints.ipg import IPGEndpoint


def test_get_token(client):
    payment = client.ipg.get_payment(1000, "https://example.com/callback")
    token = client.ipg.get_token(payment)
    assert token == client.get_request_strategy().endpoints[IPGEndpoint.token]["POST"]["response"]["token"]


def test_get_redirect_url(client):
    token = "test_token"
    redirect_url = client.ipg.get_redirect_url(token)
    assert redirect_url == IPGEndpoint.redirect.format(token=token)
