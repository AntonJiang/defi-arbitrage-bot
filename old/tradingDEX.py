from web3 import Web3
import json

# DEX UNISWAP PAIR

web3 = Web3(
    Web3.HTTPProvider("https://mainnet.infura.io/v3/ead6d3a453dd4607863e4eb840b2abe8")
)
print()
print(f"Connected: {web3.is_connected()}")

pair_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount0In",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount1In",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount0Out",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount1Out",
                "type": "uint256",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
        ],
        "name": "Swap",
        "type": "event",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {"internalType": "uint112", "name": "reserve0", "type": "uint112"},
            {"internalType": "uint112", "name": "reserve1", "type": "uint112"},
            {"internalType": "uint32", "name": "blockTimestampLast", "type": "uint32"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

token_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]


pair_address = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"

pair_contract = web3.eth.contract(address=pair_address, abi=pair_abi)

token0_address = pair_contract.functions.token0().call()
token1_address = pair_contract.functions.token1().call()

token0_contract = web3.eth.contract(address=token0_address, abi=token_abi)
token1_contract = web3.eth.contract(address=token1_address, abi=token_abi)

token0_name = token0_contract.functions.name().call()
token1_name = token1_contract.functions.name().call()

token0_decimals = token0_contract.functions.decimals().call()
token1_decimals = token1_contract.functions.decimals().call()

reserves = pair_contract.functions.getReserves().call()
reserve0 = reserves[0] / (10**token0_decimals)
reserve1 = reserves[1] / (10**token1_decimals)

print(f"Reserve for {token0_name}: {reserve0:.{token0_decimals}f}")
print(f"Reserve for {token1_name}: {reserve1:.{token1_decimals}f}")
print("-------------------------")


swap_filter = pair_contract.events.Swap.create_filter(
    fromBlock=web3.eth.block_number - 20, toBlock=web3.eth.block_number
)
events = swap_filter.get_all_entries()

# Fee rate for Uniswap V2 is 0.3% or 0.003 in decimal form
FEE_RATE = 0.003

for event in events:
    args = event["args"]

    # Token0 to Token1 swap
    if args["amount0In"] > 0 and args["amount1Out"] > 0:
        amount0_in_adjusted = args["amount0In"] / (10**token0_decimals)
        amount1_out_adjusted = args["amount1Out"] / (10**token1_decimals)

        # Predicted price impact calculation
        new_reserve0 = reserve0 + amount0_in_adjusted * (1 - FEE_RATE)
        new_reserve1 = reserve1 - amount1_out_adjusted
        predicted_price = new_reserve0 / new_reserve1

        fee = amount0_in_adjusted * FEE_RATE
        exchange_ratio = amount0_in_adjusted / amount1_out_adjusted

        print(
            f"{amount0_in_adjusted:.{token0_decimals}f} {token0_name} were exchanged for {amount1_out_adjusted:.{token1_decimals}f} {token1_name}"
        )
        print(f"Trading Fee: {fee:.{token0_decimals}f} {token0_name}")
        print(
            f"Exchange Rate: 1 {token0_name} = {exchange_ratio:.{token1_decimals}f} {token1_name}"
        )
        print(
            f"Predicted Price Impact: 1 {token0_name} = {predicted_price:.{token1_decimals}f} {token1_name} after swap"
        )
        print("-------------------------")

    # Token1 to Token0 swap
    elif args["amount1In"] > 0 and args["amount0Out"] > 0:
        amount1_in_adjusted = args["amount1In"] / (10**token1_decimals)
        amount0_out_adjusted = args["amount0Out"] / (10**token0_decimals)

        # Predicted price impact calculation
        new_reserve1 = reserve1 + amount1_in_adjusted * (1 - FEE_RATE)
        new_reserve0 = reserve0 - amount0_out_adjusted
        predicted_price = new_reserve1 / new_reserve0

        fee = amount1_in_adjusted * FEE_RATE
        exchange_ratio = amount1_in_adjusted / amount0_out_adjusted

        print(
            f"{amount1_in_adjusted:.{token1_decimals}f} {token1_name} were exchanged for {amount0_out_adjusted:.{token0_decimals}f} {token0_name}"
        )
        print(f"Trading Fee: {fee:.{token1_decimals}f} {token1_name}")
        print(
            f"Exchange Rate: 1 {token1_name} = {exchange_ratio:.{token0_decimals}f} {token0_name}"
        )
        print(
            f"Predicted Price Impact: 1 {token1_name} = {predicted_price:.{token0_decimals}f} {token0_name} after swap"
        )
        print("-------------------------")
