from pydantic import BaseModel, constr, conint


class NftMint(BaseModel):
    """Class used to validate the content you want to use to create an NFT.

    You can pass the dictionary with the content to the NftMint class like this:
    data_dict = {"name": ..., "symbol": ..., "amount": ..., "data": ...}
    NftMint(**data_dict)

    If you have an error like a name longer than 30, the call to NftMint(**data_dict) will raise a ValidationError
    """
    name: constr(max_length=30, min_length=1)
    symbol: constr(max_length=5, min_length=2)
    amount: conint(ge=1)
    data: constr(regex=r"^ipfs:\/\/ipfs\/.*")
