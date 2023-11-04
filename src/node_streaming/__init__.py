import os
import time
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

NODE_URL = os.getenv("NODE_URL")
if not NODE_URL:
    raise ValueError("Must set NODE_URL in environment variables")
else:
    print(f"Using NODE_URL: {NODE_URL}")

@dataclass
class ContractEvent:
    address: str
    abi: object
    event: str

class NodeStreaming:
    def __init__(self):
        print("Initializing NodeStreaming...")
        self.w3 = Web3(Web3.HTTPProvider(NODE_URL))
        if not self.w3.is_connected():
            raise ConnectionError("Unable to connect to the node at URL: " + NODE_URL)
        else:
            print("Connected to Ethereum node.")

        self.events_queue = []
        self.events_filters = []
    
    def get_latest_block_number(self):
        return self.w3.eth.block_number
    
    def fetch_contract_abi(self, contract_address: str):
        if contract_address == "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0":
            return [{
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "amount0In", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "amount1In", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "amount0Out", "type": "uint256"},
                    {"indexed": False, "internalType": "uint256", "name": "amount1Out", "type": "uint256"},
                    {"indexed": True, "internalType": "address", "name": "to", "type": "address"}
                ],
                "name": "Swap",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": False, "internalType": "uint112", "name": "reserve0", "type": "uint112"},
                    {"indexed": False, "internalType": "uint112", "name": "reserve1", "type": "uint112"}
                ],
                "name": "Sync",
                "type": "event"
            }]
        else:
            # Handle other contract addresses as needed or raise an exception if the address is unknown
            raise ValueError(f"No ABI found for contract address {contract_address}")


    def start_monitor(self, start_block_number: int, watching_contracts: dict[str, list[str]]):
        print(f"Starting monitor from block {start_block_number}...")
        self.events_queue = []
        for contract_address, events in watching_contracts.items():
            contract_abi = self.fetch_contract_abi(contract_address)
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            for event_name in events:
                event_filter = getattr(contract.events, event_name).create_filter(fromBlock=start_block_number)
                print(f"Monitoring for {event_name} events at address {contract_address}")
                self.events_filters.append(event_filter)

    def refresh(self):
        print("Refreshing events...")
        for filter in self.events_filters:
            new_entries = filter.get_new_entries()
            if new_entries:
                print(f"Found {len(new_entries)} new events.")
            self.events_queue.extend(new_entries)

    def poll(self):
        print("Polling for events...")
        while not self.events_queue:
            self.refresh()
            time.sleep(1)  # Wait for a short time before trying to refresh again
        event = self.events_queue.pop(0)
        print(f"Polled event: {event}")
        return event

    def stop(self):
        print("Stopping NodeStreaming...")
        self.events_filters.clear()

if __name__ == "__main__":
    print("Starting the NodeStreaming service...")

    node_stream = NodeStreaming()
    latest_block_number = node_stream.get_latest_block_number()
    watching_contracts = {
        "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0": ["Swap", "Sync"],
    }
    node_stream.start_monitor(start_block_number=latest_block_number, watching_contracts=watching_contracts)
    event = node_stream.poll()
    print(f"Event: {event}")
    node_stream.stop()
    print("NodeStreaming service has stopped.")
