from tests.helpers import MockRequestStrategy
from vandarpy.client import VandarClient
from vandarpy.endpoints.buisiness import BusinessEndpoint
import pytest


def test_get_business(client):
    b = client.business.info
    assert b.to_dict() == client.get_request_strategy().endpoints[BusinessEndpoint.info.format(name="test")]["GET"]["response"]["data"]


def test_get_business_iam(client):
    iam = client.business.iam
    assert iam.to_dict()['users'] == client.get_request_strategy().endpoints[BusinessEndpoint.iam.format(name="test")]["GET"]["response"]['data']["users"]


def test_get_wallet(client):
    wallet = client.business.wallet
    assert wallet.to_dict() == client.get_request_strategy().endpoints[BusinessEndpoint.balance.format(name="test")]["GET"]["response"]["data"]
