# hathor-sdk
[![Python package testing](https://github.com/Tall1n/hathor-sdk/actions/workflows/github-action.yml/badge.svg)](https://github.com/Tall1n/hathor-sdk/actions/workflows/github-action.yml)

python sdk for interaction with the hathor blockchain. Pull requests are welcome.

# Usage

The package contains of a collection of utility functions.

## get_nft_owner

Get the address currently holding a specific NFT

```python
from hathorsdk.get_nft_owner import get_nft_owner

nft_uid = "000000002be1e670ea340bfa244eb87b23970197852a800b68619748eb810c8b"

get_nft_owner(nft_uid)
```

## get_received_htr_amount

Get the amount of hathor sent to a specific wallet with a transaction. If the tx does not contain hathor, the function
will return an error.

```python
from hathorsdk.get_received_htr_amount import get_received_htr_amount

# tx contains 0.01 HTR
tx_id = "00000000f1e5259986d3182982afb2c535a02e45635739ee2e4033812369a919"
target_wallet = "HFVpboLjDKXjukGs5ddkp1fkmegR5wsfWE"

get_received_htr_amount(tx_id, target_wallet)
```

## get_configuration_string

Get the configuration string from a minted NFT.

```python
from hathorsdk.get_configuration_string import get_configuration_string

uid = "000000002be1e670ea340bfa244eb87b23970197852a800b68619748eb810c8b"
name = "Anubian #1631"
symbol = "A1631"

get_configuration_string(uid, name, symbol)

```

## HeadlessWallet

See [the Hathor Headless-Wallet Github Repository](https://github.com/HathorNetwork/hathor-wallet-headless) for more
information about starting the headless wallet.

Connect to the headless hathor wallet running locally in the background.

```python
from hathorsdk.headless_wallet import HeadlessWallet

headless_wallet = HeadlessWallet(base_url="http://localhost:8000")
headless_wallet.start()
headless_wallet.status
```

Send 1 HTR

```python
from hathorsdk.headless_wallet import HeadlessWallet

headless_wallet = HeadlessWallet(base_url="http://localhost:8000")
headless_wallet.start()

post_data = {
    "address": "HFEkN7Wu6X6AoeF4CvwfLGCgviUqifvnoG",
    "value": 100,
}
res = headless_wallet.send_simple_htr_tx(post_data)
```

Send an NFT

```python
from hathorsdk.headless_wallet import HeadlessWallet

headless_wallet = HeadlessWallet(base_url="http://localhost:8000")
headless_wallet.start()

nft_uid = "An NFT contained in the headless wallet that was started in the background."
transaction_data = {
    "address": "HFEkN7Wu6X6AoeF4CvwfLGCgviUqifvnoG",
    "value": 1,
    "token": nft_uid,
}

# send out the NFT
res = headless_wallet.send_simple_htr_tx(transaction_data)
```

## Pinata

To have decentralized storage and a credible NFT. You can use IPFS to store the NFT content.
[pinata.cloud](pinata.cloud) provides a service greatly simplifying the interaction with IPFS, its worth it.

You need to create a JWT token on the pinata website and use it to initialize the Pinata class.

```python
from hathorsdk.pinata import Pinata

token_string = "tokenstring "

pinata = Pinata(jwt_token=token_string)
pinata.check_api_connection()

```

Upload a local image to ipfs using pinata

```python
from hathorsdk.pinata import Pinata

token_string = "tokenstring "
pinata = Pinata(jwt_token=token_string)

local_path = "path/to/local/nft/image.png"
res_image_upload = pinata.ipfs_upload(local_path)
```

Upload a whole directory to ipfs using pinata.

```python
from hathorsdk.pinata import Pinata

token_string = "tokenstring "
pinata = Pinata(jwt_token=token_string)

local_path = "path/to/local/nft/"
res_image_upload = pinata.ipfs_upload_directory(local_path)
```

Giving a path like this will create a nested folder like that on ipfs. If you want to have only one level, you can
change the working directory for the upload like in the following example.

```python
import os

from pathlib import Path

from hathorsdk.pinata import Pinata

token_string = "tokenstring "
pinata = Pinata(jwt_token=token_string)

local_path = "path/to/local/nft/"

# save current working directory
workdir = os.getcwd()

# change the working directory to "path/to/local/"
video_directory_path = Path(local_path)
os.chdir(video_directory_path.parent)

# upload the "/nft/" directory to ipfs
ipfs_pin_response = pinata.ipfs_upload_directory(video_directory_path.name)
ipfs_hash_json = ipfs_pin_response.json()

# change back to the original working directory
os.chdir(workdir)
```

## Putting it all together in one method to mint and NFT

For my ai-nubians project 

(https://t.me/ai_nubians_chat, Mint 01.01.2022 - 31.01.2022)

I have created a processing function that goes through all steps for minting an NFT for a given anubian id. 

The basic steps are:

1. Create the NFT image / video (not in the pipeline code below)
2. IPFS upload of the image/video using pinata
3. Create the NFT metadata
4. Upload NFT metadata to IPFS using pinata
5. Mint NFT to Hathor

You will have to create your own version of the functions yourself to match your NFT project.


```python
# Pseudocode, do not run
def process_ainubian_nft(anub_id, nft_type, headless_wallet):

    # 1. create NFT image/video in another process
    
    # 2. ipfs upload NFT image
    print("IPFS upload NFT image / video.")
    ipfs_hash_json = ipfs_upload_nft_content(anub_id, nft_type)

    # 3. create the nft metadata in the format required (validate via NftMetadata class)
    print("Create NFT metadata.")
    attributes = get_ainubian_nft_metadata(anub_id)
    name = get_name(anub_id, nft_type)
    description = get_description(anub_id, nft_type)
    ipfs_hash = ipfs_hash_json["IpfsHash"]
    metadata = nft_metadata(name, description, ipfs_hash, attributes)

    # 4. ipfs upload nft metadata
    print("IPFS upload NFT metadata.")
    ipfs_hash_metadata_json = ipfs_upload_file(metadata)

    # 5. mint hft to hathor by linking to the metadata saved on ipfs.  (validate via NftMint class)
    print("HATHOR MINT NFT.")
    ipfs_hash = ipfs_hash_metadata_json["IpfsHash"]
    prefix = get_prefix(nft_type)
    nft_resp_json = mint_ainubian_nft(ipfs_hash, headless_wallet, prefix=prefix)

    return nft_resp_json
```

# local development

For virtual env management Pipenv is used.

Clone the repo, install pipenv and run `pipenv install --dev` to install the package in development mode.

# packaging and pushing to pypi

Don't forget to adjust the calendar version to the current date.

```shell
pipenv run python -m build --sdist
```

Test Pypi:

```shell
pipenv run twine upload --repository testpypi dist/* -u __token__ -p $TEST_PYPI_TOKEN --verbose
```

Real PyPi:

```shell
pipenv run twine upload dist/* -u __token__ -p $PYPI_TOKEN --verbose
```

