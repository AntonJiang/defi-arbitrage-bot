import abc

from src.data_processing.trading_path import TradingPath


class ArbStrategy(abc.ABC):

    starting_tokens: list[str]

    def __init__(self):
        self.starting_tokens = self.get_flashloan_tokens()

    def get_flashloan_tokens(self) -> list[str]:
        """
        returns a list of flashloanable tokens, these tokens needs to be the start of the path
        :return:
        """
        # TODO (hard code @andy)
        pass

    @abc.abstractmethod
    def compute_optimal_path(self, trading_paths: list[TradingPath]):
        pass


class BruteForceArbStrategy(ArbStrategy):
    """
    TODO
    """

    pass
