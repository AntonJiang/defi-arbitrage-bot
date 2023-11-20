import abc

from src.data_processing.trading_path import TradingPath
from src.db.trading_path_db import TradingPathDB
from src.flashloan.providers import FlashloanProvider


class ExecutionPlan:
    initial_token_amount: int
    final_token_amount: int
    flashloan_provider: FlashloanProvider
    trading_paths: list[TradingPath]


class ArbStrategy(abc.ABC):
    starting_tokens: list[str]

    flashloan_providers: list[FlashloanProvider]
    trading_path_db: TradingPathDB

    def __init__(
        self,
        flashloan_providers: list[FlashloanProvider],
        trading_path_db: TradingPathDB,
    ):
        self.flashloan_providers = flashloan_providers
        self.starting_tokens = self.get_flashloan_tokens(self.flashloan_providers)
        self.trading_path_db = trading_path_db

    @staticmethod
    def get_flashloan_tokens(providers: list[FlashloanProvider]) -> list[str]:
        """
        returns a list of flashloanable tokens, these tokens needs to be the start of the path
        :return:
        """
        flashloan_tokens = []

        for provider in providers:
            flashloan_tokens.extend(provider.supported_tokens)

        return flashloan_tokens

    @abc.abstractmethod
    def compute_optimal_path(self) -> ExecutionPlan:
        pass


class BruteForceArbStrategy(ArbStrategy):
    """ """

    def compute_optimal_path(self) -> ExecutionPlan:
        """
        TODO
        compute the best trading path we can have here.

        Use, trading_path_db to get current trading path information
        :param trading_paths:
        :return:
        """
        best_plan = None
        best_profit = -float('inf')

        def search_best_path(current_token, start_token, current_amount, current_plan, current_profit):
            nonlocal best_plan, best_profit

            if current_token == start_token and current_plan.trading_paths:
                if current_profit > best_profit:
                    best_profit = current_profit
                    best_plan = current_plan.copy()
                return

            possible_trades = self.trading_path_db.load_path_by_token(current_token)

            for trade in possible_trades:
                next_token = trade.token_1 if trade.token_0 == current_token else trade.token_0
                price_update = trade.calculate_price(current_amount)
                new_amount = price_update.token_1_out
                profit = new_amount - current_amount

                if profit > 0:
                    new_plan = ExecutionPlan(
                        initial_token_amount=current_plan.initial_token_amount,
                        final_token_amount=new_amount,
                        flashloan_provider=current_plan.flashloan_provider,
                        trading_paths=current_plan.trading_paths + [trade]
                    )
                    search_best_path(next_token, start_token, new_amount, new_plan, current_profit + profit)

        for token in self.starting_tokens:
            initial_plan = ExecutionPlan(
                initial_token_amount=0,
                final_token_amount=0,
                flashloan_provider=None,
                trading_paths=[]
            )
            search_best_path(token, token, 1, initial_plan, 0)

        return best_plan
            


