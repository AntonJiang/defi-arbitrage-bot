from src.arb_strategy import ExecutionPlan
from src.data_processing.trading_path import TradingPath, UniswapV2TradingPath
from src.node_streaming.web3_pool import Web3Pool
from src.transaction_execution import TransactionExecutor
import pytest
from pprint import pprint

@pytest.fixture()
def te():
    w3_pool = Web3Pool()
    t = TransactionExecutor(w3_pool)
    yield t


def test_bytes_parsing(te: TransactionExecutor):
    b = te.to_bytes("0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11", ["0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
                                                                   "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11"])

    assert b == "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11b4e16d0168e52d35cacd2c6185b44281ec28c9dca478c2975ab1ea89e8196811f51a7b7ade33eb11"


def test_simulation(te: TransactionExecutor):
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    initial_amount = 100e18

    simulate_plan = ExecutionPlan(
        initial_token_amount=initial_amount,
        final_token_amount=-1,
        token=DAI,
        flashloan_provider=None,
        trading_paths=[UniswapV2TradingPath(
            protocol_name="",
            contract_address="0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11",
            token_0="",
            token_1="",
            reserve_0=0,
            reserve_1=0,
        ), UniswapV2TradingPath(
            protocol_name="",
            contract_address="0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
            token_0="",
            token_1="",
            reserve_0=0,
            reserve_1=0,
        ), UniswapV2TradingPath(
            protocol_name="",
            contract_address="0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5",
            token_0="",
            token_1="",
            reserve_0=0,
            reserve_1=0,
        )]

    )

    result = te.simulate_transaction(simulate_plan)
    pprint(result)
