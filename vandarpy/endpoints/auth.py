from vandarpy.utils.decorators import endpoint


@endpoint(label="Auth")
class AuthEndpoint:
    refresh_token = ""
