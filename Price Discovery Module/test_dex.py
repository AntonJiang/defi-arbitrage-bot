# test_price_discovery.py

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
