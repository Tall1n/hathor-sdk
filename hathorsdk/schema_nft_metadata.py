from typing import List

from pydantic import BaseModel, constr


class Attribute(BaseModel):
    type: str
    value: str


class NftMetadata(BaseModel):
    name: constr(max_length=30, min_length=1)
    description: str
    file: constr(regex=r"^ipfs:\/\/ipfs\/.*")
    attributes: List[Attribute]
