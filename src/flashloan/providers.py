import abc

from src.node_streaming.abi import ERC20_balance_of
from src.node_streaming.web3_pool import Web3Pool


class FlashloanProvider:
    name: str
    supported_tokens: list[str]
    fee_percentage: float

    @abc.abstractmethod
    def get_max_token_supported(self, web3: Web3Pool, token: str):
        pass

    @abc.abstractmethod
    def get_flashloan_params(self, token: str, amount: int):
        pass


def reverse_dict(input_dict):
    return {value: key for key, value in input_dict.items()}


class AaveFlashloanProvider(FlashloanProvider):
    name = "aave"
    fee_percentage = 0.0005

    a_tokens = {
        "0x4d5F47FA6A74757f35C14fD3a6Ef8E3C9BC514E8": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "0x0B925eD163218f6662a35e0f0371Ac234f9E9371": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
        "0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "0x018008bfb33d285247A21d44E50697654f754e63": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "0x5E8C8A7243651DB1384C0dDfDbE39761E8e7E51a": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        "0xA700b4eB416Be35b2911fd5Dee80678ff64fF6C9": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    }

    reverse_a_tokens = reverse_dict(a_tokens)

    def __init__(self):
        self.supported_tokens = list(self.a_tokens.values())

    def get_flashloan_params(self, token: str, amount: int):
        raise NotImplementedError

    def get_max_token_supported(self, web3: Web3Pool, token: str):
        return web3.read_contract(token, ERC20_balance_of, "balanceOf", [self.reverse_a_tokens[token]])
