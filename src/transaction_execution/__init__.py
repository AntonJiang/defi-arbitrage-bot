import dataclasses
from typing import Tuple, Any

from web3 import Web3, middleware
from web3.exceptions import ContractLogicError
from web3.gas_strategies.time_based import fast_gas_price_strategy

from src.arb_strategy import ExecutionPlan
from src.node_streaming.web3_pool import Web3Pool
from src.transaction_execution.abi import DEPLOY_CODE, ABI


@dataclasses.dataclass
class SimulationResult:
    profitable: bool
    profit: float
    initial_amount: int
    final_amount: int
    final_amount_w_flashfee: int


@dataclasses.dataclass
class ExecutionResult:
    status: bool
    transaction_hash: str


class TransactionExecutor:
    """
    TODO, does 2 things 1. execute a transaciton. 2. simulate a transaction from a list of trading path & flashloan pick
    """
    deploy_code: str = DEPLOY_CODE
    contract_address = Web3.to_checksum_address("0x1000000000000000000000000000000000000000")
    caller_address = Web3.to_checksum_address("0x2000000000000000000000000000000000000000")

    def __init__(self, w3: Web3Pool):
        self.w3 = w3.web3
        self.contract = self.w3.eth.contract(self.contract_address, abi=ABI)
        self.w3.eth.set_gas_price_strategy(fast_gas_price_strategy)

        self.w3.middleware_onion.add(middleware.time_based_cache_middleware)
        self.w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        self.w3.middleware_onion.add(middleware.simple_cache_middleware)

    def execute_transaction(self, plan: ExecutionPlan) -> ExecutionResult:
        # TODO
        pass

    def gas_estimation(self, plan: ExecutionPlan) -> tuple[int, int]:
        """
        return the ETH gas cost of this plan based on current gas price
        """
        estimated_gas_price = int(self.w3.eth.generate_gas_price())

        txParam = self.contract.functions.uniswapV2SwapTest(
            int(plan.initial_token_amount), plan.token, [addr.contract_address for addr in plan.trading_paths]
        ).build_transaction({
            "from": self.caller_address
        })
        estimate_gas_params = {
            'transaction': txParam,
            'stateOverride': {
                    self.contract_address: {
                        "code": self.deploy_code
                    }
                }
        }
        estimated_gas = self.w3.provider.make_request('eth_estimateGas', [estimate_gas_params])
        estimated_gas = int(estimated_gas["result"], 16)
        return estimated_gas, estimated_gas_price

    def simulate_transaction(self, plan: ExecutionPlan, block_number="latest") -> SimulationResult:
        try:
            res = self.contract.functions.uniswapV2SwapTest(
                int(plan.initial_token_amount), plan.token, [addr.contract_address for addr in plan.trading_paths]
            ).call(
                transaction={
                    "from": self.caller_address,
                    "to": self.contract_address,
                },
                block_identifier=block_number,
                state_override={
                    # our contract
                    self.contract_address: {
                        "code": self.deploy_code
                    }
                },
            )
        except ContractLogicError as e:
            print(e)
            raise e

        final_with_fee = res - plan.initial_token_amount * 0.0005

        return SimulationResult(
            profitable=final_with_fee > plan.initial_token_amount,
            profit=final_with_fee - plan.initial_token_amount,
            initial_amount=plan.initial_token_amount,
            final_amount=res,
            final_amount_w_flashfee=final_with_fee,
        )

    @staticmethod
    def to_bytes(start_token, pathes):
        start_token = Web3.to_checksum_address(start_token)
        pathes = [Web3.to_checksum_address(addr) for addr in pathes]
        # Convert start_token to its bytes representation
        start_token_bytes = Web3.to_bytes(hexstr=start_token)

        # Initialize data with start_token_bytes
        data = start_token_bytes

        # Convert each address in pathes to bytes and concatenate
        for path in pathes:
            path_bytes = Web3.to_bytes(hexstr=path)
            data += path_bytes

        return "0x" + data.hex()
