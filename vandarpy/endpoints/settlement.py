from vandarpy.utils.decorators import endpoint


@endpoint(label='Settlement', aliases={'store': 'create'})
class SettlementEndpoint:
    list = ""
    banks = ""
    create = ""
