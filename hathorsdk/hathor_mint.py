"""Mint the ipfs metadata onto the hathor blockchain.

The Headless Wallet has to be running in the background to access the /mint-nft endpoint.
"""

import json

import requests

from hathorsdk.schema_hathor_mint import NftMint
from hathorsdk.schema_nft_metadata import NftMetadata


def mint_nft(metadata_ipfs_hash, symbol, headless_wallet):
    res = requests.get(f'https://ipfs.io/ipfs/{metadata_ipfs_hash}')
    res_json = res.json()
    # validate the NFT data content to be sure it's a valid hathor NFT
    _ = NftMetadata(**res_json)

    name = res_json["name"]
    nft_data = {
        "name": name,
        "symbol": symbol,
        "amount": 1,
        "data": f"ipfs://ipfs/{metadata_ipfs_hash}",
    }

    # Validate the body for the NFT mint
    _ = NftMint(**nft_data)

    nft_resp = headless_wallet.create_nft(nft_data)
    nft_resp_json = nft_resp.json()
    if not nft_resp_json["success"]:
        raise ValueError(
            f"The creation of NFT {name} Failed.\nThe api response was:\n{json.dumps(nft_resp_json, indent=4)}"
        )

    return nft_resp_json
