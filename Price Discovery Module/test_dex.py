import pytest
from tradingDEXv2 import *

def test_price_discovery_module_simple():
    trading_path = TradingPath(
        token0_name="TokenA",
        token1_name="TokenB",
        token0_decimals=18,
        token1_decimals=18,
        reserve0=1000,
        reserve1=500
    )

    token_0_in = 10

    result = PriceDiscoveryModule.calculate_price_update(trading_path, token_0_in)
    print(result)
    
    assert isinstance(result, PriceUpdate)
    assert result.trading_path == trading_path

    assert result.optimal_price_ratio == 2.0  # Because 1000/500 = 2
    assert result.token_0_in == token_0_in

    k = trading_path.reserve0 * trading_path.reserve1
    amount0_in_adjusted = token_0_in * (1 - PriceDiscoveryModule.FEE_RATE)
    new_reserve0 = trading_path.reserve0 + amount0_in_adjusted
    new_reserve1 = k / new_reserve0
    expected_token_1_out = trading_path.reserve1 - new_reserve1
    expected_actual_price_ratio = amount0_in_adjusted / expected_token_1_out

    assert result.token_1_out == pytest.approx(expected_token_1_out, 0.01)  # allow a small delta for floating point imprecision
    assert result.actual_price_ratio == pytest.approx(expected_actual_price_ratio, 0.01)

