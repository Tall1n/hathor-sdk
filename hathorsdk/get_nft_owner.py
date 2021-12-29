import requests


def get_nft_owner(token_uid: str, base_url="https://node.explorer.hathor.network/v1a") -> str:
    """Get the address currently holding the given NFT."""
    tokensResponse = requests.get(
        f"{base_url}/thin_wallet/token_history",
        params={"id": token_uid, "count": 1},
    )
    res_json = tokensResponse.json()

    transactions_output = res_json["transactions"][0]["outputs"]
    address_holding_the_token = [
        tx["decoded"]["address"]
        for tx in transactions_output
        if tx["token"] == token_uid
    ]

    return address_holding_the_token[0]
