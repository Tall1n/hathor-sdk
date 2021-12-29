from pytest import raises

from hathorsdk.get_received_htr_amount import get_received_htr_amount


def test_get_received_htr_amount():
    """0.01 HTR was sent from HD5uDhnLr9ZFeX3kmLCA9CofG43n5Lr3KW to
    HFVpboLjDKXjukGs5ddkp1fkmegR5wsfWE which created the transaction id
    00000000f1e5259986d3182982afb2c535a02e45635739ee2e4033812369a919
    """
    # arrange
    tx_id = "00000000f1e5259986d3182982afb2c535a02e45635739ee2e4033812369a919"  # contains 0.01 HTR
    target_wallet = "HFVpboLjDKXjukGs5ddkp1fkmegR5wsfWE"

    expected_amount = 1

    # act
    res = get_received_htr_amount(tx_id, target_wallet)

    # assert
    assert res == expected_amount


def test_get_received_amount_received():
    """A transaction containing more than 0.01 HTR."""
    # arrange
    tx_id = "00000000c5d0ad8ae2361de1c0caa9bed0285cff35a5fd989238ba1dc8fc8ae5"
    target_wallet = "HPc1Ev21oqC3cVUTbzN92J5t28FdAtQG72"

    expected_amount = 139

    # act
    res = get_received_htr_amount(tx_id, target_wallet)

    # assert
    assert res == expected_amount


def test_get_received_amount_nft_error():
    # arrange
    tx_id = "00000000fc12b9091f861f12615d428a6bd5c67545451778bfbc7118d1ab6373"
    target_wallet = "HPc1Ev21oqC3cVUTbzN92J5t28FdAtQG72"

    # act
    with raises(ValueError) as ve:
        _ = get_received_htr_amount(tx_id, target_wallet)

    assert "The transaction contains no Hathor." in str(ve.value)


def test_get_received_amount_norse_token_error():
    # arrange
    tx_id = "0000000011e3c7c99b5ed0467a08c42250a6080855e3a3a7588c573781a9bb65"
    target_wallet = "H8kVwBwx42a9jJL5Bh2MujApNFpvWoYGQs"

    # act
    with raises(ValueError) as ve:
        _ = get_received_htr_amount(tx_id, target_wallet)

    # assert
    assert "The transaction contains no Hathor." in str(ve.value)
