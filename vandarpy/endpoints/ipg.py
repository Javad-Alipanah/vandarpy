from vandarpy.utils.decorators import endpoint


@endpoint(label="IPG", aliases={'send': 'token', 'transaction_info': 'info'})
class IPGEndpoint:
    token = ""
    info = ""
    redirect = "/v3/{token}"
