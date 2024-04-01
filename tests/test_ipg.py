from vandarpy.endpoints.ipg import IPGEndpoint


def test_get_token(client):
    payment = client.ipg.get_payment(1000, "https://example.com/callback")
    token = client.ipg.get_token(payment)
    assert token == client.get_request_strategy().endpoints[IPGEndpoint.token]["POST"]["response"]["token"]


def test_get_redirect_url(client):
    token = "test_token"
    redirect_url = client.ipg.get_redirect_url(token)
    assert redirect_url == IPGEndpoint.redirect.format(token=token)


def test_get_transaction_info(client):
    token = "test_token"
    transaction = client.ipg.get_transaction_info(token)
    assert transaction.is_successful()
    assert transaction.is_card_number_valid("1234123412341238")
    assert transaction.to_dict() == client.get_request_strategy().endpoints[IPGEndpoint.info]["POST"]["response"]


def test_verify_transaction(client):
    token = "test_token"
    transaction = client.ipg.verify_transaction(token)
    assert transaction.is_successful()
    assert transaction.to_dict() == client.get_request_strategy().endpoints[IPGEndpoint.verify]["POST"]["response"]
