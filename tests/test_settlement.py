from vandarpy.endpoints.settlement import SettlementEndpoint


def test_settlement_list(client):
    settlements = client.business.settlements
    for i, settlement in enumerate(settlements):
        assert settlement.to_dict() == client.get_request_strategy().endpoints[
            SettlementEndpoint.list.format(business="test")
        ]["GET"]["response"]["data"]["settlements"]["data"][i]


def test_settlement_banks(client):
    banks = client.business.banks
    for i, bank in enumerate(banks):
        assert bank.to_dict() == client.get_request_strategy().endpoints[
            SettlementEndpoint.banks.format(business="test")
        ]["GET"]["response"]["data"][i]


def test_request_settlement(client):
    response = client.business.request_settlement(1000, "IR", 1234)
    for i in range(len(response)):
        assert response[i].to_dict() == client.get_request_strategy().endpoints[
            SettlementEndpoint.create.format(business="test")
        ]["POST"]["response"]["data"]["settlement"][i]


def test_get_settlement(client):
    settlement = client.business.get_settlement("12345678-1234-1234-1234-123456789012")
    assert settlement.to_dict() == client.get_request_strategy().endpoints[
        SettlementEndpoint.get.format(business="test", settlement_id="12345678-1234-1234-1234-123456789012")
    ]["GET"]["response"]["data"]["settlement"]
