from src.data_processing.trading_path import TradingPath
from src.data_processing.trading_path import UniswapV2TradingPath
from src.data_processing.typings import PriceUpdate

from web3 import Web3



class DataParser:
    # TODO (write data parser here, parse into TradingPath objects) @sofia, @victor
    # communicate with node streaming module to grab all the information needed to parse

    """
    Main function is given a raw log and knowing the contract address, parse into corresponding trading path objects

    """


    def getLogs(self, contract_address: str, *args):
        #get logs from contract address 
        web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/273183394e5344799f454dd8f8d37d18'))
        
        pool_address = contract_address
        #right now abi is hardcoded TODO: fix that 
        abi = [{"anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "recipient", "type": "address"},
        {"indexed": False, "internalType": "int256", "name": "amount0", "type": "int256"},
        {"indexed": False, "internalType": "int256", "name": "amount1", "type": "int256"},
        {"indexed": False, "internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
        {"indexed": False, "internalType": "uint128", "name": "liquidity", "type": "uint128"},
        {"indexed": False, "internalType": "int24", "name": "tick", "type": "int24"}], "name": "Swap", "type": "event"}]
        
        contract = web3.eth.contract(address=pool_address, abi=abi)
        
        logs = contract.events.Swap.create_filter(fromBlock='latest').get_all_entries()
        
        return logs

    def parse(self, contract_address: str, *args) -> TradingPath:
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
        trading_path = TradingPath(UniswapV2TradingPath, contract_address, sender, recipient, amount0, amount1)
        return trading_path

    

    
    










