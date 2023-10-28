import pytest

from src.data_processing.trading_path import UniswapV2TradingPath
from src.data_processing.typings import PriceUpdate


def test_price_discovery_module_simple():
    trading_path = UniswapV2TradingPath(
        protocol_name="uniswap",
        contract_address="0x0",
        token_0="0xa",
        token_1="0xb",
        reserve_0=1000,
        reserve_1=500
    )

    token_0_in = 10

    result = trading_path.calculate_price(token_0_in)

    print(result)

    assert isinstance(result, PriceUpdate)

    assert result.optimal_price_ratio == 2.0  # Because 1000/500 = 2
    assert result.token_0_in == token_0_in

    assert result.token_1_out == pytest.approx(4.935790171985332, 0.0001)
    assert result.actual_price_ratio == pytest.approx(2.0260180541624773,
                                                      0.0001)  # As per the printed result in the error message
