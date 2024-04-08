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
        assert response[i].to_dict() == client.get_request_strategy().endpoints[SettlementEndpoint.create.format(business="test")][
            "POST"]["response"]["data"]["settlement"][i]
