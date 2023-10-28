class NodeStreaming:
    """
    TODO @will Adjust signatures as needed.
    This modules takes in a list of contract addresses and their corresponding log events to watch.


    """

    def __init__(self):
        pass

    def start_monitor(self, start_block_number: int, watching_contracts: dict[str, list[str]]):
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