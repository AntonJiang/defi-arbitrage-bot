def get_event_abi(
        event_name: str,
        contract_address: str = None,
):
    """
    Assume all events are the same across contracts
    :param contract_address:
    :param event_name:
    :return:
    """

    if event_name == "Swap":
        return [
            {"anonymous": False,
             "inputs": [{"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
                        {"indexed": True, "internalType": "address", "name": "recipient", "type": "address"},
                        {"indexed": False, "internalType": "int256", "name": "amount0", "type": "int256"},
                        {"indexed": False, "internalType": "int256", "name": "amount1", "type": "int256"},
                        {"indexed": False, "internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
                        {"indexed": False, "internalType": "uint128", "name": "liquidity", "type": "uint128"},
                        {"indexed": False, "internalType": "int24", "name": "tick", "type": "int24"}], "name": "Swap",
             "type": "event"}
        ]
    elif event_name == "Sync":
        return [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": False,
                        "internalType": "uint112",
                        "name": "reserve0",
                        "type": "uint112",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint112",
                        "name": "reserve1",
                        "type": "uint112",
                    },
                ],
                "name": "Sync",
                "type": "event",
            }
        ]
    else:
        # Handle other contract addresses as needed or raise an exception if the address is unknown
        raise ValueError(f"No ABI found for contract address {event_name}")
