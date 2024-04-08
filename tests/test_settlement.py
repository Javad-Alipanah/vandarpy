from vandarpy.endpoints.settlement import SettlementEndpoint


def test_settlement_list(client):
    settlements = client.business.settlements
    assert all(
        settlement.to_dict() ==
        client.get_request_strategy().endpoints[SettlementEndpoint.list.format(business="test")]["GET"]["response"][
            "data"]["settlements"]["data"][i] for i, settlement in enumerate(settlements)
    )


def test_settlement_banks(client):
    banks = client.business.banks
    assert all(
        bank.to_dict() ==
        client.get_request_strategy().endpoints[SettlementEndpoint.banks.format(business="test")]["GET"]["response"][
            "data"][i] for i, bank in enumerate(banks)
    )
