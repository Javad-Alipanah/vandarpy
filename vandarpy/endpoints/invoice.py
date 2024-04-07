from vandarpy.utils.decorators import endpoint


@endpoint(label="Invoice", aliases={"business_wallet_balance": "balance", "business_transactions_report": "transactions"})
class InvoiceEndpoint:
    balance = ""
    transactions = ""
