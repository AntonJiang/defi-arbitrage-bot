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
        pass
