import logging

import requests


class HeadlessWallet(object):
    """Hathor Headless Wallet Connection.
    Github Docs for basic functionality: https://github.com/HathorNetwork/hathor-wallet-headless
    Full, up-to-date swagger docs: https://wallet-headless.docs.hathor.network/

    Run `npm start` in path/to/cloned/git/repo/hathor-wallet-headlesst.
    Follow the Github Docs to get the wallet started with a seed phrase.
    """

    def __init__(
            self,
            base_url="http://localhost:8000",
            wallet_id="123",
            api_key="123",
    ):
        self.wallet_id = wallet_id
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-Wallet-Id": self.wallet_id, "X-API-KEY": self.api_key}

    @property
    def status(self):
        status = requests.get(f"{self.base_url}/wallet/status", headers=self.headers)
        return status

    def start(self, wallet_id=None):
        if wallet_id is None:
            wallet_id = self.wallet_id
        start_data = {"wallet-id": wallet_id, "seedKey": "default"}
        logging.info(f"Starting wallet with {wallet_id=}")
        start = requests.post(
            f"{self.base_url}/start",
            headers=self.headers,
            data=start_data,
        )
        if not start.json() == {"success": True}:
            raise ConnectionError("Could not start headless wallet.")

    def balance(self, token_id=None):
        if token_id is not None:
            params = {"token_id": token_id}
        else:
            params = {}
        balance_url = f"{self.base_url}/wallet/balance"
        balance = requests.get(balance_url, headers=self.headers, params=params)
        return balance

    def address(self, mark_as_used=None):
        if mark_as_used is not None:
            params = {"mark_as_used": mark_as_used}
        else:
            params = {}

        address_url = f"{self.base_url}/wallet/address"
        address = requests.get(address_url, headers=self.headers, params=params)
        return address

    def addresses(self):
        addresses_url = f"{self.base_url}/wallet/addresses"
        addresses = requests.get(addresses_url, headers=self.headers)
        return addresses

    def tx_history(self):
        tx_history_url = f"{self.base_url}/wallet/tx-history"
        tx_history = requests.get(tx_history_url, headers=self.headers)
        return tx_history

    def send_tx(self, transaction_data):
        """Send Transactions.
        transaction_data: List[Dict]
        Example transaction_data:
        {
            "outputs": [
                {
                "address": "Wk2j7odPbC4Y98xKYBCFyNogxaRimU6BUj",
                "value": 1,
                "token": "006e18f3c303892076a12e68b5c9c30afe9a96a528f0f3385898001858f9c35d"
                }
            ],
            "inputs": [
                {
                "hash": "006e18f3c303892076a12e68b5c9c30afe9a96a528f0f3385898001858f9c35d",
                "index": 0
                }
            ]
        }
        """
        raise NotImplementedError("Sending multiple transactions is not yet implemented")
        transaction_url = f"{self.base_url}/wallet/send-tx"
        transaction = requests.post(
            transaction_url,
            headers=self.headers,
            json={"outputs": transaction_data},
        )

        return transaction

    def send_simple_htr_tx(self, transaction_data):
        """Send Transactions.
        transaction_data: List[Dict]
        Example transaction_data:
        {
            "address": "Wk2j7odPbC4Y98xKYBCFyNogxaRimU6BUj",
            "value": 100,
        }
        """
        transaction_url = f"{self.base_url}/wallet/simple-send-tx"
        transaction = requests.post(
            transaction_url,
            headers=self.headers,
            json=transaction_data,
        )

        return transaction

    def create_nft(self, nft_data):
        """Create an NFT token.
        nft_data = {
          "name": "Test Coin",
          "symbol": "TSC",
          "amount": 100,
          "data": "ipfs://ipfs/myNFTHash/filename"
        }

        """
        create_nft_url = f"{self.base_url}/wallet/create-nft"
        create_nft = requests.post(create_nft_url, headers=self.headers, json=nft_data)
        return create_nft
