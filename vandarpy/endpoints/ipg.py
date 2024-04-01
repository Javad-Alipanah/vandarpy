from vandarpy.utils.decorators import endpoint


@endpoint(base_url="https://ipg.vandar.io")
class IPGEndpoint:
    token = "/api/v3/send"
    redirect = "/v3/{token}"
    info = "/api/v3/transaction"
    verify = "/api/v3/verify"
