from vandarpy.utils.decorators import endpoint


@endpoint(base_url="https://api.vandar.io")
class EndpointBase:
    refresh_token = "/v3/refreshtoken/"
