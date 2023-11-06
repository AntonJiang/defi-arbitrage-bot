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
            }
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
