from vandarpy.endpoints.base import EndpointBase
from vandarpy.utils.decorators import endpoint


@endpoint(base_url="/v2/business/", base_class=EndpointBase)
class BusinessEndpoint:
    info = "/{name}"
    # Identity and Access Management
    iam = "/{name}/iam"
