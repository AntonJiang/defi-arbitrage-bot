from dataclasses import dataclass


@dataclass
class PriceUpdate:
    optimal_price_ratio: float
    actual_price_ratio: float
    token_0_in: int
    token_1_out: int
    trading_fee: float
