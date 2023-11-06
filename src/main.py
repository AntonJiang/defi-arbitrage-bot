from dotenv import load_dotenv
import os

from src.arb_strategy import ArbStrategy, BruteForceArbStrategy, ExecutionPlan
from src.data_processing.raw_parser import DataParser
from src.data_processing.trading_path import TradingPath
from src.db.trading_path_db import InMemoryTradingPathDB
from src.flashloan.providers import FlashloanProvider, AaveFlashloanProvider
from src.node_streaming import NodeStreaming, ContractEventDefinition, ContractEvent
from src.transaction_execution import (
    TransactionExecutor,
    SimulationResult,
    ExecutionResult,
)


class Bot:
    node: NodeStreaming
    flashloan_providers: list[FlashloanProvider]
    arb_calculator: ArbStrategy
    transaction_executor: TransactionExecutor

    def __init__(
        self,
        watching_events: list[ContractEventDefinition],
        flashloan_providers: list[FlashloanProvider],
    ):
        self.node = NodeStreaming(
            os.environ["NODE_URL"], watching_contracts=watching_events
        )
        self.flashloan_providers = flashloan_providers

        self.data_parser = DataParser()

        self.trading_path_db = InMemoryTradingPathDB()

        self.arb_calculator = BruteForceArbStrategy(
            self.flashloan_providers, self.trading_path_db
        )

        self.transaction_executor = TransactionExecutor()

    def run(self):
        while True:
            latest_raw_events: ContractEvent = self.node.poll()

            trading_path: TradingPath = self.data_parser.parse(latest_raw_events)

            self.trading_path_db.save_path(trading_path)

            execution_plan: ExecutionPlan = self.arb_calculator.compute_optimal_path()

            print(f"possible execution plan: {execution_plan}")
            if (
                execution_plan.final_token_amount - execution_plan.initial_token_amount
                <= 0
            ):
                continue

            simulation_result: SimulationResult = (
                self.transaction_executor.simulate_transaction(execution_plan)
            )

            print(f"simulation result: {simulation_result}")

            if not simulation_result.profitable:
                continue

            execution_result: ExecutionResult = (
                self.transaction_executor.execute_transaction(execution_plan)
            )
            print(f"execution result: {execution_result}")

        self.close()

    def close(self):
        self.node.stop()


if __name__ == "__main__":
    load_dotenv()

    watching_contracts = [
        ContractEventDefinition("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Sync")
    ]
    # TODO: hardcode a more comprehensive list of contract event definitions, more LPs, just Sync

    flashloan_providers = [AaveFlashloanProvider()]
    arb_bot = Bot(
        watching_events=watching_contracts, flashloan_providers=flashloan_providers
    )

    arb_bot.run()
