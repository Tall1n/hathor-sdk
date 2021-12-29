from hathorsdk.get_configuration_string import get_configuration_string


def test_get_configuration_string():
    """On the explorer the nft can be found here.

    https://explorer.hathor.network/token_detail/000000002be1e670ea340bfa244eb87b23970197852a800b68619748eb810c8b
    """
    # arrange
    uid = "000000002be1e670ea340bfa244eb87b23970197852a800b68619748eb810c8b"
    name = "Anubian #1631"
    symbol = "A1631"

    # act
    res = get_configuration_string(uid, name, symbol)

    # assert
    assert res == '[Anubian #1631:A1631:000000002be1e670ea340bfa244eb87b23970197852a800b68619748eb810c8b:be6b9898]'
