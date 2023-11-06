import os
import time
from dataclasses import dataclass
from typing import Optional

from web3 import Web3

from src.data_processing.abi import get_event_abi


@dataclass
class ContractEventDefinition:
    address: str
    event: str


@dataclass
class ContractEvent:
    raw_event: dict
    definition: ContractEventDefinition


@dataclass
class ContractEventFilter:
    definition: ContractEventDefinition
    event_filter: object


class NodeStreaming:
    def __init__(
        self,
        node_url: str,
        watching_contracts: list[ContractEventDefinition],
        start_block: Optional[int] = None,
    ):
        print("Initializing NodeStreaming...")
        self.w3 = Web3(Web3.HTTPProvider(node_url))

        if not self.w3.is_connected():
            raise ConnectionError("Unable to connect to the node at URL: " + node_url)
        else:
            print("Connected to Ethereum node.")

        self.events_queue: list[ContractEvent] = []
        self.events_filters: list[ContractEventFilter] = []

        if start_block is None:
            start_block = self.get_latest_block_number()

        self.init_event_filters(start_block, watching_contracts)

    def get_latest_block_number(self) -> int:
        return self.w3.eth.block_number

    def init_event_filters(
        self, start_block_number: int, watching_contracts: list[ContractEventDefinition]
    ):
        for contract_def in watching_contracts:
            event_name = contract_def.event
            contract = self.w3.eth.contract(
                address=contract_def.address, abi=get_event_abi(event_name)
            )
            event_filter = getattr(contract.events, event_name).create_filter(
                fromBlock=start_block_number
            )
            print(
                f"Monitoring for {event_name} events at address {contract_event.address}"
            )
            self.events_filters.append(
                ContractEventFilter(event_filter=event_filter, definition=contract_def)
            )

    def refresh(self):
        print("Refreshing events...")
        for contract_event_filter in self.events_filters:
            contract_def = contract_event_filter.contract_def
            event_filter = contact_event_filter.event_filter
            new_entries = event_filter.get_new_entries()
            if new_entries:
                print(f"Found {len(new_entries)} new events.")
            for new_entry in new_entries:
                self.events_queue.append(
                    ContractEvent(definition=contract_def, raw_event=new_entry)
                )

    def poll(self) -> ContractEvent:
        print("Polling for events...")
        while not self.events_queue:
            self.refresh()
            time.sleep(5)  # Wait for a short time before trying to refresh again
        event = self.events_queue.pop(0)
        print(f"Polled event: {event.raw_event}")
        return event

    def stop(self):
        print("Stopping NodeStreaming...")
        self.events_filters.clear()


if __name__ == "__main__":
    print("Starting the NodeStreaming service...")

    node_stream = NodeStreaming(
        os.getenv("NODE_URL"),
        watching_contracts=[
            ContractEventDefinition(
                "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Swap"
            ),
            ContractEventDefinition(
                "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Sync"
            ),
        ],
    )
    event = node_stream.poll()
    print(f"Event: {event}")
    node_stream.stop()
    print("NodeStreaming service has stopped.")
