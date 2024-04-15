from vandarpy.utils.decorators import endpoint


@endpoint(label="BatchSettlement", aliases={"store": "create", "show": "get"})
class BatchSettlementEndpoint:
    list = ""
    create = ""
    get = ""
