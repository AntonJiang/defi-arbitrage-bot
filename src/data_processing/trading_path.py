import abc
from dataclasses import dataclass

from src.data_processing.typings import PriceUpdate


@dataclass
class TradingPath(abc.ABC):  # abstract class
    protocol_name: str
    contract_address: str
    token_0: str
    token_1: str

    def __post_init__(self):
        if self.__class__ == TradingPath:
            raise TypeError("Cannot instantiate abstract class.")

    @abc.abstractmethod
    def calculate_price(self, token_in: int, token: str) -> PriceUpdate:
        pass


@dataclass
class UniswapV3TradingPath(TradingPath):
    reserve_0: float
    reserve_1: float
    sqrtPriceX96: float
    FEE_RATE: float = 0.003

    def calculate_price(self, token_in: int, token: str) -> PriceUpdate:
        reserve0 = self.reserve_0
        reserve1 = self.reserve_1

        k = reserve0 * reserve1

        if token == self.token_0:
            amount0_in_adjusted = token_in

            new_reserve0 = reserve0 + amount0_in_adjusted * (1 - self.FEE_RATE)
            reserve1_prime = k / new_reserve0

            amount1_out_adjusted = reserve1 - reserve1_prime

            new_reserve1 = reserve1 - amount1_out_adjusted

            predicted_price = new_reserve0 / new_reserve1

            fee = amount0_in_adjusted * self.FEE_RATE
            exchange_ratio = amount0_in_adjusted / amount1_out_adjusted

            actual_price_ratio = exchange_ratio
            optimal_price_ratio = reserve0 / reserve1

            price_update = PriceUpdate(
                optimal_price_ratio=optimal_price_ratio,
                actual_price_ratio=actual_price_ratio,
                token_in_amount=token_in,
                token_out_amount=int(amount1_out_adjusted),
                token_in=token,
                token_out=self.token_1,
                trading_fee=fee,
            )
        else:
            amount1_in_adjusted = token_in

            new_reserve1 = reserve1 + amount1_in_adjusted * (1 - self.FEE_RATE)
            reserve0_prime = k / new_reserve1

            amount0_out_adjusted = reserve0 - reserve0_prime

            new_reserve0 = reserve0 - amount0_out_adjusted

            predicted_price = new_reserve1 / new_reserve0

            fee = amount1_in_adjusted * self.FEE_RATE
            exchange_ratio = amount1_in_adjusted / amount0_out_adjusted

            actual_price_ratio = exchange_ratio
            optimal_price_ratio = reserve1 / reserve0

            price_update = PriceUpdate(
                optimal_price_ratio=optimal_price_ratio,
                actual_price_ratio=actual_price_ratio,
                token_out=self.token_0,
                token_in=self.token_1,
                token_out_amount=int(amount0_out_adjusted),
                token_in_amount=token_in,
                trading_fee=fee,
            )
        return price_update


@dataclass
class UniswapV2TradingPath(TradingPath):
    reserve_0: float
    reserve_1: float
    FEE_RATE: float = 0.003

    def calculate_price(self, token_in: int, token: str) -> PriceUpdate:
        reserve0 = self.reserve_0
        reserve1 = self.reserve_1

        k = reserve0 * reserve1

        if token == self.token_0:
            amount0_in_adjusted = token_in

            new_reserve0 = reserve0 + amount0_in_adjusted * (1 - self.FEE_RATE)
            reserve1_prime = k / new_reserve0

            amount1_out_adjusted = reserve1 - reserve1_prime

            new_reserve1 = reserve1 - amount1_out_adjusted

            predicted_price = new_reserve0 / new_reserve1

            fee = amount0_in_adjusted * self.FEE_RATE
            exchange_ratio = amount0_in_adjusted / amount1_out_adjusted

            actual_price_ratio = exchange_ratio
            optimal_price_ratio = reserve0 / reserve1

            price_update = PriceUpdate(
                optimal_price_ratio=optimal_price_ratio,
                actual_price_ratio=actual_price_ratio,
                token_in_amount=token_in,
                token_out_amount=int(amount1_out_adjusted),
                token_in=token,
                token_out=self.token_1,
                trading_fee=fee,
            )
        else:
            amount1_in_adjusted = token_in

            new_reserve1 = reserve1 + amount1_in_adjusted * (1 - self.FEE_RATE)
            reserve0_prime = k / new_reserve1

            amount0_out_adjusted = reserve0 - reserve0_prime

            new_reserve0 = reserve0 - amount0_out_adjusted

            predicted_price = new_reserve1 / new_reserve0

            fee = amount1_in_adjusted * self.FEE_RATE
            exchange_ratio = amount1_in_adjusted / amount0_out_adjusted

            actual_price_ratio = exchange_ratio
            optimal_price_ratio = reserve1 / reserve0

            price_update = PriceUpdate(
                optimal_price_ratio=optimal_price_ratio,
                actual_price_ratio=actual_price_ratio,
                token_out=self.token_0,
                token_in=self.token_1,
                token_out_amount=int(amount0_out_adjusted),
                token_in_amount=token_in,
                trading_fee=fee,
            )
        return price_update
