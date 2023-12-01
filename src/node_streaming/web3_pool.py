import os

import web3

from src.node_streaming.abi import TOKEN0_TOKEN1
import json

CACHE_FILE = 'lp_cache.txt'
class Web3Pool:
    def __init__(self):
        self.web3 = web3.Web3(web3.Web3.HTTPProvider(os.environ["NODE_URL"]))
        try:
            self.cache = json.load(open(CACHE_FILE, 'r'))
        except (IOError, ValueError):
            self.cache = {}

    def get_token0_token1(self, lp_contract):
        lp_contract = self.web3.to_checksum_address(lp_contract)
        if lp_contract in self.cache:
            return self.cache[lp_contract]
        _token0 = self.read_contract(lp_contract, TOKEN0_TOKEN1, 'token0', parameters=[])
        _token1 = self.read_contract(lp_contract, TOKEN0_TOKEN1, 'token1', parameters=[])

        self.cache[lp_contract] = (_token0, _token1)
        json.dump(self.cache, open(CACHE_FILE, 'w'))
        return _token0, _token1

    def read_contract(
            self, contract_address: str, abi: dict, function_name: str, parameters: list
    ):
        # Create a contract object using the ABI and address
        contract = self.web3.eth.contract(address=contract_address, abi=abi)

        # Ensure the function exists in the contract ABI
        if function_name not in [n.fn_name for n in contract.all_functions()]:
            # print([dir(n) for n in contract.all_functions()])
            raise ValueError(
                f"The function {function_name} is not present in the contract ABI."
            )

        # Call the function with the provided arguments
        contract_function = contract.get_function_by_name(function_name)(*parameters)

        # Make a call to the contract function, this doesn't create a transaction as it's a read call
        result = contract_function.call()

        return result
