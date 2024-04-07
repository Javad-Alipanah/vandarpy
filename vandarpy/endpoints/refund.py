from vandarpy.utils.decorators import endpoint


@endpoint(label="Refund")
class RefundEndpoint:
    refund = ""
