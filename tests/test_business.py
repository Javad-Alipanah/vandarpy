from vandarpy.endpoints.buisiness import BusinessEndpoint
from vandarpy.endpoints.invoice import InvoiceEndpoint
from vandarpy.endpoints.refund import RefundEndpoint


def test_get_business(client):
    b = client.business.info
    assert b.to_dict() == \
           client.get_request_strategy().endpoints[BusinessEndpoint.info.format(business="test")]["GET"]["response"]["data"]


def test_get_business_iam(client):
    iam = client.business.iam
    assert [u.to_dict() for u in iam] == \
           client.get_request_strategy().endpoints[BusinessEndpoint.iam.format(business="test")]["GET"]["response"]['data'][
               "users"]


def test_get_wallet(client):
    wallet = client.business.wallet
    assert wallet.to_dict() == \
           client.get_request_strategy().endpoints[InvoiceEndpoint.balance.format(business="test")]["GET"]["response"][
               "data"]


def test_get_transactions(client):
    transactions = client.business.transactions()
    for i, t in enumerate(transactions):
        assert t.to_dict() == client.get_request_strategy().endpoints[InvoiceEndpoint.transactions.format(business="test")]["GET"][
               "response"]["data"][i]


def test_refund_transaction(client):
    transaction_id = 12345
    refunds = client.business.refund(transaction_id)
    for i, refund in enumerate(refunds):
        assert refund.to_dict() == client.get_request_strategy().endpoints[
               RefundEndpoint.refund.format(business="test", transaction_id=transaction_id)
        ]["POST"]["response"]["data"]['results'][i]
