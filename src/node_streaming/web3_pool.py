import os

import web3
class Web3Pool:

    def __init__(self):
        self.web3 = web3.Web3(web3.Web3.HTTPProvider(os.environ["NODE_URL"]))

    def read_contract(self, contract_address: str, abi: dict, function_name: str,  parameters: list):
        # Create a contract object using the ABI and address
        contract = self.web3.eth.contract(address=contract_address, abi=abi)

        # Ensure the function exists in the contract ABI
        if function_name not in [n.fn_name for n in contract.all_functions()]:
            # print([dir(n) for n in contract.all_functions()])
            raise ValueError(f"The function {function_name} is not present in the contract ABI.")

        # Call the function with the provided arguments
        contract_function = contract.get_function_by_name(function_name)(*parameters)

        # Make a call to the contract function, this doesn't create a transaction as it's a read call
        result = contract_function.call()

        return result
