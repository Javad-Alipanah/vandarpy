from vandarpy.utils.decorators import endpoint


@endpoint(label='Settlement', aliases={'store': 'create', 'show': 'get'})
class SettlementEndpoint:
    list = ""
    banks = ""
    create = ""
    get = ""
