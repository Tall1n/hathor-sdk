from hathorsdk.burn_wallet_address import burn_address
from hathorsdk.get_nft_owner import get_nft_owner


def test_get_nft_owner():
    # arrange
    nft_uid = "000000002be1e670ea340bfa244eb87b23970197852a800b68619748eb810c8b"

    # act
    res = get_nft_owner(nft_uid)

    # assert
    assert res == burn_address
