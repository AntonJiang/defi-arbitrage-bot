import json
import os
import pickle
import uuid

from src.node_streaming import NodeStreaming, ContractEventDefinition

node_stream = NodeStreaming(
    os.getenv("NODE_URL", None),
    watching_contracts=[
        ContractEventDefinition("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Swap"),
        ContractEventDefinition("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Sync"),
    ],
)

event = node_stream.poll()

with open(os.path.join(os.pardir, f"test_events/{uuid.uuid4()}.pickle"), "wb") as f:
    pickle.dump(event, f, protocol=pickle.HIGHEST_PROTOCOL)
