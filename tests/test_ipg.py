from vandarpy.endpoints.ipg import IPGEndpoint


def test_get_token(client):
    payment = client.ipg.get_payment(1000, "https://example.com/callback")
    token = client.ipg.get_token(payment)
    assert token == client.get_request_strategy().endpoints[IPGEndpoint.token]["POST"]["response"]["token"]
