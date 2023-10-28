import os

from web3 import Web3

NODE_URL = os.getenv("NODE_URL", None)
if not NODE_URL:
    raise ValueError("Must set NODE_URL in environment variables")


class NodeStreaming:
    """
    TODO @will Adjust signatures as needed.
    This modules takes in a list of contract addresses and their corresponding log events to watch.
    """

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(NODE_URL))
        assert self.w3.is_connected()

    def start_monitor(
        self, start_block_number: int, watching_contracts: dict[str, list[str]]
    ):
        """
        :param start_block_number: the starting block to streaming for
        :param watching_contracts:
            a dict of contracts to a list of log events
            e.g
            {"0x012...12" : ["Swap", "Sync"],
            ...
            }
        :return:
        """
        pass

    def poll(self):
        """
        :return: returns the next log in the iteration
        """
        pass

    def stop(self):
        pass


if __name__ == "__main__":
    node_stream = NodeStreaming()
