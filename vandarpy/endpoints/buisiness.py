from vandarpy.utils.decorators import endpoint


@endpoint(label="Business", aliases={'users': 'iam'})
class BusinessEndpoint:
    info = ""
    iam = ""
