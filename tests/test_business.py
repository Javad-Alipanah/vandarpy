from tests.helpers import MockRequestStrategy
from vandarpy.client import VandarClient
from vandarpy.endpoints.buisiness import BusinessEndpoint


def test_get_business():
    mock_req_strategy = MockRequestStrategy()
    client = VandarClient(
        token="token",
        refresh_token="refresh_token",
    )
    client.set_request_strategy(mock_req_strategy)
    b = client.business.info("test")
    assert b.to_dict() == mock_req_strategy.endpoints[BusinessEndpoint.info.format(name="test")]["GET"]["response"]["data"]


def test_get_business_iam():
    mock_req_strategy = MockRequestStrategy()
    client = VandarClient(
        token="token",
        refresh_token="refresh_token",
    )
    client.set_request_strategy(mock_req_strategy)
    iam = client.business.iam("test")
    assert iam.to_dict()['users'] == mock_req_strategy.endpoints[BusinessEndpoint.iam.format(name="test")]["GET"]["response"]['data']["users"]
