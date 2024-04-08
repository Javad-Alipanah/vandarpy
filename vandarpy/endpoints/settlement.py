from vandarpy.utils.decorators import endpoint


@endpoint(label='Settlement', aliases={'store': 'create', 'show': 'get', 'destroy': 'cancel'})
class SettlementEndpoint:
    list = ""
    banks = ""
    create = ""
    get = ""
    cancel = ""
