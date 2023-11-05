import dataclasses

from src.arb_strategy import ExecutionPlan


@dataclasses.dataclass
class SimulationResult:
    profitable: bool
    profit: float
    profit_token: str


@dataclasses.dataclass
class ExecutionResult:
    status: bool
    transaction_hash: str


class TransactionExecutor:
    """
    TODO, does 2 things 1. execute a transaciton. 2. simulate a transaction from a list of trading path & flashloan pick
    """

    def execute_transaction(self, plan: ExecutionPlan) -> ExecutionResult:
        # TODO
        pass

    def simulate_transaction(self, plan: ExecutionPlan) -> SimulationResult:
        # TODO
        pass
