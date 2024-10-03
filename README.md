# Witness API Python Client

This is a Python client library for interacting with the [Witness API](https://docs.witness.co/). It provides convenient methods to access both core and utility endpoints of the Witness API, allowing you to integrate Witness functionalities into your Python applications seamlessly.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Initializing the Client](#initializing-the-client)
  - [Available Methods](#available-methods)
  - [Example Usage](#example-usage)
- [Error Handling](#error-handling)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Easy-to-use Python client for the Witness API.
- Supports both authenticated and unauthenticated endpoints.
- Handles API errors gracefully with detailed exception handling.
- Includes methods for core functionalities like inserting leaf hashes and verifying proofs.
- Utility methods for retrieving checkpoints, leaf indices, timestamps, and more.

## Installation

To use the Witness API Python Client, ensure you have Python 3.6 or higher installed. Install the required dependencies using pip:

```bash
pip install requests
```

## Usage
### Initializing the client

First, import the `WitnessClient` class from your module and initialize it:

```python
from witness_client import WitnessClient

# Initialize the client without authentication
client = WitnessClient()

# If you need to access authenticated endpoints, provide your bearer token
token = 'your_bearer_token_here'
auth_client = WitnessClient(token=token)
```

### Available Methods

The `WitnessClient` class provides the following methods:

#### Health Check
- `health()`: Check the health status of the API.

#### Checkpoint Methods
- `get_latest_checkpoint(chainId: int = 8453)`: Get the latest on-chain checkpoint for a specific chain.
- `get_latest_checkpoint_for_all_chains()`: Get the latest on-chain checkpoints for all chains.
- `get_earliest_checkpoint_covering_leaf_index(leafIndex: str, chainId: int = 8453)`: Get the earliest checkpoint covering a specific leaf index.
- `get_checkpoint_by_transaction_hash(txHash: str)`: Get a checkpoint by its transaction hash.
- `get_checkpoint_by_timestamp(timestamp: str, chainId: int = 8453)`: Get the first checkpoint at or after a Unix timestamp.

#### Leaf and Node Methods
- `get_leaf_index_by_hash(leafHash: str)`: Get the leaf index by its hash.
- `get_timestamp_by_leaf_hash(leafHash: str, chainId: int = 8453)`: Get the timestamp associated with a leaf hash.
- `get_node_hash_by_id(level: str, index: str)`: Get the node hash by level and index.

#### Proof Methods
- `get_proof_for_leaf_hash(leafHash: str, targetTreeSize: Optional[str] = None, chainId: int = 8453)`: Get the proof for a given leaf hash.
- `post_proof(proof_data: Dict[str, Any])`: Verify a proof.

#### Tree State
- `get_tree_state()`: Get the current state of the tree.

#### Insert Leaf Hash (Authenticated)
- `post_leaf_hash(leafHash: str)`: Insert a new leaf hash into the tree.

### Example Usage

```python
from witness_client import WitnessClient, WitnessError

if __name__ == "__main__":
    # Initialize the client
    client = WitnessClient()

    try:
        # Health check
        health = client.health()
        print("Health:", health)

        # Get the latest checkpoint
        latest_checkpoint = client.get_latest_checkpoint()
        print("Latest Checkpoint:", latest_checkpoint)

        # Get the latest checkpoints for all chains
        all_checkpoints = client.get_latest_checkpoint_for_all_chains()
        print("All Checkpoints:", all_checkpoints)

        # Get earliest checkpoint covering a specific leaf index
        leaf_index = "1234"
        checkpoint = client.get_earliest_checkpoint_covering_leaf_index(leaf_index)
        print(f"Checkpoint covering leaf index {leaf_index}:", checkpoint)

        # Get checkpoint by transaction hash
        tx_hash = "0x2cf28b31b91c4a50e3eb5093a4db60f3a41cd21568f304ff654eafdafc7e88ab"
        checkpoint_by_tx = client.get_checkpoint_by_transaction_hash(tx_hash)
        print(f"Checkpoint for transaction {tx_hash}:", checkpoint_by_tx)

        # Get checkpoint by timestamp
        timestamp = "1724284172"
        checkpoint_by_time = client.get_checkpoint_by_timestamp(timestamp)
        print(f"Checkpoint at or after timestamp {timestamp}:", checkpoint_by_time)

        # Get leaf index by hash
        leaf_hash = "0x97e78047a64a1bb484d69e3093ec34d9a0d13f682496bffa492626909df5efd3"
        leaf_index_data = client.get_leaf_index_by_hash(leaf_hash)
        print(f"Leaf index for hash {leaf_hash}:", leaf_index_data)

        # Get timestamp by leaf hash
        timestamp_data = client.get_timestamp_by_leaf_hash(leaf_hash)
        print(f"Timestamp for leaf hash {leaf_hash}:", timestamp_data)

        # Get node hash by ID
        level = "1"
        index = "0"
        node_hash = client.get_node_hash_by_id(level, index)
        print(f"Node hash at level {level}, index {index}:", node_hash)

        # Get proof for leaf hash
        proof = client.get_proof_for_leaf_hash(leaf_hash)
        print(f"Proof for leaf hash {leaf_hash}:", proof)

        # Verify proof
        proof_data = {
            "leftHashes": proof.get("leftHashes", []),
            "rightHashes": proof.get("rightHashes", []),
            "targetRootHash": proof.get("targetRootHash"),
            "leafHash": proof.get("leafHash"),
            "leafIndex": proof.get("leafIndex"),
        }
        verification_result = client.post_proof(proof_data)
        print("Proof verification result:", verification_result)

        # Get tree state
        tree_state = client.get_tree_state()
        print("Tree state:", tree_state)

        # Insert a new leaf hash (requires authentication)
        token = "your_bearer_token_here"
        auth_client = WitnessClient(token=token)
        new_leaf_hash = "0xabc123..."
        insertion_result = auth_client.post_leaf_hash(new_leaf_hash)
        print("Insertion result:", insertion_result)

    except WitnessError as e:
        print(f"Witness API Error: {e}")
    except Exception as e:
        # Handle other exceptions such as network errors
        print(f"An unexpected error occurred: {e}")
```

Note: Replace `"your_bearer_token_here"` with your actual bearer token when accessing authenticated endpoints.

## Error handling

The client includes robust error handling through the custom `WitnessError` exception class. All methods can raise a `WitnessError` if an error occurs during the API call. The `WitnessError` exception provides:

- **message**: A descriptive error message.
- **code**: An optional error code returned by the API.
- **issues**: An optional list of issues or validation errors.

Example of handling errors:

```python
from witness_client import WitnessClient, WitnessError

client = WitnessClient()

try:
    latest_checkpoint = client.get_latest_checkpoint()
except WitnessError as e:
    print(f"Witness API Error: {e}")
    # Additional error handling...
```

## Dependencies
- **Python**: 3.6 or higher
- **Requests Library**: Used for HTTP requests

Install dependencies using:

``` bash
pip install requests
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full text.
