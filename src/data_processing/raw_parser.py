from src.data_processing.trading_path import TradingPath


class DataParser:
    # TODO (write data parser here, parse into TradingPath objects) @sofia, @victor
    # communicate with node streaming module to grab all the information needed to parse

    """
    Main function is given a raw log and knowing the contract address, parse into corresponding trading path objects

    """

    def parse(self, contract_address: str, *args) -> TradingPath:
        pass