import abc
import dataclasses

from src.data_processing.trading_path import TradingPath
from src.db.trading_path_db import TradingPathDB
from src.flashloan.providers import FlashloanProvider


@dataclasses.dataclass
class ExecutionPlan:
    initial_token_amount: int
    final_token_amount: int
    token: str
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


@dataclasses.dataclass
class IntermediateTrade:
    trades: list[TradingPath]
    traded_contracts: set[str]
    current_token: str
    flashloan_provider: FlashloanProvider


class BruteForceArbStrategy(ArbStrategy):
    """ """

    def compute_optimal_path(self) -> ExecutionPlan:
        """
        compute the best trading path we can have here.
        Use, trading_path_db to get current trading path information
        :param trading_paths:
        :return:
        """
        possible_trading_path: list[IntermediateTrade] = []

        for provider in self.flashloan_providers:
            for starting_token in provider.supported_tokens:
                possible_trades = self.trading_path_db.load_path_by_token(starting_token)

                intermediate_trades = [IntermediateTrade(
                    trades=[t],
                    traded_contracts={t.contract_address},
                    current_token=t.token_0 if t.token_1 == starting_token else t.token_1,
                    flashloan_provider=provider)
                    for t in possible_trades]
                # list for keep track of trades made so far, set for avoid making the same trades.
                # we'll remove the path once it's not valid for reached end
                while len(intermediate_trades) != 0:
                    path_processing = intermediate_trades.pop(0)
                    _next_possible_trades = self.trading_path_db.load_path_by_token(path_processing.current_token)

                    # filter out trades already done
                    _next_possible_trades = [_t for _t in _next_possible_trades if
                                             _t.contract_address not in path_processing.traded_contracts]

                    if len(_next_possible_trades) == 0:
                        continue

                    _next_trades = [IntermediateTrade(
                        path_processing.trades + [_t],
                        set(list(path_processing.traded_contracts) + [_t.contract_address]),
                        current_token=_t.token_0 if _t.token_1 == path_processing.current_token else _t.token_1,
                        flashloan_provider=provider
                    ) for _t in _next_possible_trades]

                    for _t in _next_trades:
                        if _t.current_token == starting_token:
                            possible_trading_path.append(_t)
                        else:
                            intermediate_trades.append(_t)

        possible_execution_plans = []
        # find out the optimal amount: TODO not hard code an amount
        for path in possible_trading_path:
            # hardcode trade 2 % of the first LP
            first_lp = path.trades[0]
            start_token_reserve = first_lp.reserve_0 if first_lp.token_0 == path.current_token else first_lp.reserve_1
            initial_trade_amount = start_token_reserve * 0.02
            current_token_amount = initial_trade_amount
            current_token = path.current_token
            for _trade_path in path.trades:
                price_update = _trade_path.calculate_price(current_token_amount, current_token)

                current_token = price_update.token_out
                current_token_amount = price_update.token_out_amount

            possible_execution_plans.append(ExecutionPlan(
                initial_token_amount=initial_trade_amount,
                final_token_amount=current_token_amount,
                token=path.current_token,
                flashloan_provider=path.flashloan_provider,
                trading_paths=path.trades
            ))
        max_profit_percentage = 0
        max_profit_plan = None
        for plan in possible_execution_plans:
            profit_percentage = plan.final_token_amount / plan.initial_token_amount

            if profit_percentage > max_profit_percentage:
                max_profit_plan = plan
                max_profit_percentage = profit_percentage

        return max_profit_plan
