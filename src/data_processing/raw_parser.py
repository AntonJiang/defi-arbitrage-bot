from src.data_processing.trading_path import TradingPath, UniswapV3TradingPath
from src.data_processing.trading_path import UniswapV2TradingPath
from src.data_processing.typings import PriceUpdate

from web3 import Web3

from src.node_streaming import ContractEvent
from src.node_streaming.web3_pool import Web3Pool


class DataParser:
    """
    Given a raw log and knowing the contract address, parse into corresponding trading path objects
    """
    def __init__(self, w3: Web3Pool):
        self.w3 = w3

    def parse(self, event: ContractEvent) -> TradingPath:
        """Returns a TradingPath parsed from a ContractEvent"""
        definition = event.definition
        raw_event = event.raw_event

        if definition.event == 'Sync':
            token0, token1 = self.w3.get_token0_token1(definition.address)
            # producing UniswapV2TradingPath
            trading_path = UniswapV2TradingPath(
                protocol_name="uniswapv2",
                contract_address=definition.address,
                token_0=token0,
                token_1=token1,
                reserve_0=raw_event.args.reserve0,
                reserve_1=raw_event.args.reserve1,
            )
        elif definition.event == 'Swap':
            token0, token1 = self.w3.get_token0_token1(definition.address)

            trading_path = UniswapV3TradingPath(
                protocol_name="uniswapv3",
                contract_address=definition.address,
                token_0=token0,
                token_1=token1,
                sqrtPriceX96=raw_event.args.sqrtPriceX96,
                reserve_0=abs(raw_event.args.amount0),
                reserve_1=abs(raw_event.args.amount1),
            )
        else:
            raise NotImplementedError
        return trading_path

    def parse_many(self, events: list[ContractEvent]) -> list[TradingPath]:
        trading_paths: list[UniswapV2TradingPath] = []
        for event in events:
            trading_paths.append(self.parse(event))
        return trading_paths
