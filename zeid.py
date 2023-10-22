from web3 import Web3

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/my_adress'))

pool_address = '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640'

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
print(logs)
