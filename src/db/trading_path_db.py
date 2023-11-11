import abc

from src.data_processing.trading_path import TradingPath


class TradingPathDB:
    """
    High level db wrapper
    """

    @abc.abstractmethod
    def save_path(self, trading_path: TradingPath):
        pass

    @abc.abstractmethod
    def load_all_path(self) -> list[TradingPath]:
        pass

    @abc.abstractmethod
    def load_path_by_token(self, token_address: str) -> list[TradingPath]:
        """
        Return all trading path of that involves this token
        :param token_address:
        :return:
        """
        pass


class InMemoryTradingPathDB(TradingPathDB):
    trading_path: list

    def __init__(self):
        self.trading_path = []

    def save_path(self, trading_path: TradingPath):
        self.trading_path.append(trading_path)

    def load_all_path(self) -> list[TradingPath]:
        return list(self.trading_path)

    def load_path_by_token(self, token_address: str) -> list[TradingPath]:
        return [path for path in self.trading_path if path.token_0 == token_address or path.token_1 == token_address]
