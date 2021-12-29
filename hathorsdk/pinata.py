import os

import requests
from requests import Response


class Pinata(object):
    """A helper class used for interacting with pinata.cloud to upload nft content to ipfs.

    Not all functionality pinata provides is implemeted yet.
    """

    def __init__(self, jwt_token):
        self.headers = {"Authorization": f'Bearer {jwt_token}'}
        self.base_url = "https://api.pinata.cloud"

    def check_api_connection(self) -> None:
        status_url = f"{self.base_url}/data/testAuthentication"
        res = requests.get(status_url, headers=self.headers)
        success_message = "Congratulations! You are communicating with the Pinata API!"
        if not res.json()["message"] == success_message:
            raise ConnectionError("Could not connect to Pinata API.")

    def ipfs_upload(self, file_path: str) -> Response:
        pin_url = f"{self.base_url}/pinning/pinFileToIPFS"
        files = {"file": open(file_path, "rb")}
        res = requests.post(f"{pin_url}", headers=self.headers, files=files)
        return res

    def ipfs_upload_directory(self, dir_path: str) -> Response:
        pin_url = f"{self.base_url}/pinning/pinFileToIPFS"
        all_files = [os.path.join(dir_path, filename) for filename in os.listdir(dir_path)]
        files = [("file", (file, open(file, "rb"))) for file in all_files]

        res = requests.post(f"{pin_url}", headers=self.headers, files=files)
        return res
