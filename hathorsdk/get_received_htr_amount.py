import json

import requests


def get_received_htr_amount(tx_id, target_wallet, base_url="https://node.explorer.hathor.network/v1a"):
    """Get the Amount of Hathor sent to the target_wallet.

    Currently, only Hathor Token is valid, no other Token.
    """
    tx_response = requests.get(
        f"{base_url}/transaction",
        params={"id": tx_id, "type": "tx", "count": 1000},
    )
    res_json = tx_response.json()
    if res_json["tx"]["tokens"]:
        raise ValueError(f"The transaction contains no Hathor. The response is:\n{json.dumps(res_json, indent=4)}")

    # get all transactions going to the target_wallet
    tx_outputs = res_json["tx"]["outputs"]
    decoded_tx_outputs = [output["decoded"] for output in tx_outputs if output["decoded"]]
    relevant_decoded_tx = [output for output in decoded_tx_outputs if output["address"] == target_wallet]
    if not relevant_decoded_tx:
        raise KeyError(f"The transaction {tx_id} does not contain a transaction to the address {target_wallet}")

    # get all transactions containing HTR (other tokens are not accepted)
    htr_tx = [output for output in relevant_decoded_tx if output["token_data"] == 0]
    if not htr_tx:
        raise KeyError(f"The transaction {tx_id} does not contain a HTR transaction to the address {target_wallet}")

    # get the received HTR amount in 0.01 increments
    received_amount = [output["value"] for output in htr_tx]

    return sum(received_amount)
