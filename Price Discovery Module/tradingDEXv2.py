from dataclasses import dataclass

@dataclass
class TradingPath:
    token0_name: str
    token1_name: str
    token0_decimals: int
    token1_decimals: int
    reserve0: float
    reserve1: float

@dataclass
class PriceUpdate:
    trading_path: TradingPath
    optimal_price_ratio: float
    actual_price_ratio: float
    token_0_in: float
    token_1_out: float
    trading_fee: float


class PriceDiscoveryModule:
    FEE_RATE = 0.003

    @staticmethod
    def calculate_price_update(trading_path: TradingPath, token_0_in: float) -> PriceUpdate:
        reserve0 = trading_path.reserve0
        reserve1 = trading_path.reserve1

        k = reserve0 * reserve1

        amount0_in_adjusted = token_0_in

        new_reserve0 = reserve0 + amount0_in_adjusted * (1 - PriceDiscoveryModule.FEE_RATE)
        reserve1_prime = k / new_reserve0

        amount1_out_adjusted = reserve1 - reserve1_prime

        new_reserve1 = reserve1 - amount1_out_adjusted
        
        predicted_price = new_reserve0 / new_reserve1

        fee = amount0_in_adjusted * PriceDiscoveryModule.FEE_RATE
        exchange_ratio = amount0_in_adjusted / amount1_out_adjusted

        actual_price_ratio = exchange_ratio
        optimal_price_ratio = reserve0 / reserve1

        price_update = PriceUpdate(
            trading_path=trading_path,
            optimal_price_ratio=optimal_price_ratio,
            actual_price_ratio=actual_price_ratio,
            token_0_in=token_0_in,
            token_1_out=amount1_out_adjusted,
            trading_fee=fee
        )

        return price_update

trading_path = TradingPath(
    token0_name="Token0",
    token1_name="Token1",
    token0_decimals=18,
    token1_decimals=5,
    reserve0=1000.0,
    reserve1=500.0
)

token_0_in = 10.0
price_update = PriceDiscoveryModule.calculate_price_update(trading_path, token_0_in)
print(price_update)
