from src.node_streaming.uniswap_v2_pool import UniswapV2PoolFinder
from src.node_streaming.web3_pool import Web3Pool
from dotenv import load_dotenv

load_dotenv()
def test_uniswap_v2_finder():
    w3 = Web3Pool()
    finder = UniswapV2PoolFinder(w3)
    finder.find_pools("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")