from dataclasses import dataclass


@dataclass
class PriceUpdate:
    optimal_price_ratio: float
    actual_price_ratio: float
    token_in_amount: int
    token_out_amount: int
    token_in: str
    token_out: str
    trading_fee: float
