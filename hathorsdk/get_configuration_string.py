import hashlib
from typing import Dict


def get_nft_configuration_string(nft_resp_json: Dict) -> str:
    name = nft_resp_json["name"]
    symbol = nft_resp_json["symbol"]
    uid = nft_resp_json["hash"]
    return get_configuration_string(uid, name, symbol)


def get_configuration_string(uid: str, name: str, symbol: str) -> str:
    """uid, name and symbol can be found in the `hathorsdk.hathor_mint.mint_nft()` response."""
    partial_config = f"{name}:{symbol}:{uid}"
    checksum = get_checksum(partial_config)
    return f"[{partial_config}:{checksum}]"


def get_checksum(partial_config: str) -> str:
    result = hashlib.sha256(partial_config.encode())
    return hashlib.sha256(result.digest()).hexdigest()[:8]
