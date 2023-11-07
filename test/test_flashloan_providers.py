from src.flashloan.providers import AaveFlashloanProvider
from src.node_streaming.web3_pool import Web3Pool


def test_flashloan_provider():
    w3 = Web3Pool()

    flashloan = AaveFlashloanProvider()

    print(flashloan.get_max_token_supported(w3, flashloan.supported_tokens[0]))
