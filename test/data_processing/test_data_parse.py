import pickle

from src.data_processing.raw_parser import DataParser


def test_data_parser():
    with open("../test_events/8e1493d5-c241-454c-b34a-ff675fddb075.pickle", "rb") as f:
        event = pickle.load(f)
        print(event.definition)

        parser = DataParser()
        path = parser.parse(event)

        print(path)
        assert path.contract_address == "0x1111111254EEB25477B68fb85Ed929f73A960582"


if __name__ == "__main__":
    test_data_parser()
