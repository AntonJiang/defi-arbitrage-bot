from src.data_processing.trading_path import TradingPath
from src.data_processing.trading_path import UniswapV2TradingPath
from src.data_processing.typings import PriceUpdate

from web3 import Web3

from src.node_streaming import ContractEvent


class DataParser:
    """
    Given a raw log and knowing the contract address, parse into corresponding trading path objects
    """

    def parse(self, event: ContractEvent) -> TradingPath:
        """Returns a TradingPath parsed from a ContractEvent"""
        defintion = event.definition
        raw_event = event.raw_event
        args = raw_event.args

        sender = args.sender
        recipient = args.recipient
        amount0 = args.amount0
        amount1 = args.amount1
        sqrtPriceX96 = args.sqrtPriceX96
        liquidity = args.liquidity
        tick = args.tick

        # May be useful in the future
        logIndex = raw_event.logIndex
        transactionIndex = raw_event.transactionIndex
        transactionHash = raw_event.transactionHash
        address = raw_event.address
        blockHash = raw_event.blockHash
        blockNumber = raw_event.blockNumber

        # Make TradinPath from this data
        trading_path = UniswapV2TradingPath(
            definition.address, sender, recipient, amount0, amount1
        )
        return trading_path

    def parse_many(self, events: list[ContractEvent]) -> list[TradingPath]:
        trading_paths: list[UniswapV2TradingPath] = []
        for event in events:
            trading_paths.append(self.parse(event))
        return trading_paths
