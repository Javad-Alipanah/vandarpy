from vandarpy.endpoints.base import EndpointBase
from vandarpy.utils.decorators import endpoint


@endpoint(base_url="/", base_class=EndpointBase)
class BusinessEndpoint:
    info = "/v2/business/{name}"
    # Identity and Access Management
    iam = "/v2/business/{name}/iam"
    # invoice
    balance = "/v2/business/{name}/balance"

    transactions = "/v3/business/{name}/transaction"
