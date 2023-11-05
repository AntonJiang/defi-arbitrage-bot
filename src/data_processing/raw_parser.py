from src.data_processing.trading_path import TradingPath
from src.data_processing.trading_path import UniswapV2TradingPath
from src.data_processing.typings import PriceUpdate

from web3 import Web3

from src.node_streaming import ContractEvent


class DataParser:
    # TODO (write data parser here, parse into TradingPath objects) @sofia, @victor
    # communicate with node streaming module to grab all the information needed to parse

    """
    Main function is given a raw log and knowing the contract address, parse into corresponding trading path objects

    """

    def parse(self, event: ContractEvent) -> TradingPath:
        """
        TODO
        :return:
        """
        logs = getLogs(self, contract_address, *args)

        #now that we have the logs, we need to parse all the information from it 
        sender = logs[0].args.sender
        recipient = logs[0].args.recipient
        amount0 = logs[0].args.amount0
        amount1 = logs[0].args.amount1
        sqrtPriceX96 = logs[0].args.sqrtPriceX96
        liquidity = logs[0].args.liquidity
        tick = logs[0].args.tick

        logIndex = logs[0].logIndex
        transactionIndex = logs[0].transactionIndex
        transactionHash = logs[0].transactionHash
        address = logs[0].address
        blockHash = logs[0].blockHash
        blockNumber = logs[0].blockNumber

        #make Trading path from this data 
        trading_path = UniswapV2TradingPath(contract_address, sender, recipient, amount0, amount1)
        return trading_path

    

    
    










