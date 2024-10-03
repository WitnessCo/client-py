import requests
from typing import Optional, Dict, Any

class WitnessError(Exception):
    """Custom exception class for Witness API errors."""
    def __init__(self, message: str, code: Optional[str] = None, issues: Optional[list] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.issues = issues or []

    def __str__(self):
        base_message = f"{self.message}"
        if self.code:
            base_message += f"\nError Code: {self.code}"
        if self.issues:
            base_message += "\nIssues:"
            for issue in self.issues:
                base_message += f"\n - {issue.get('message')}"
        return base_message

class WitnessClient:
    def __init__(self, base_url: str = 'https://api.witness.co', token: Optional[str] = None):
        """
        Initialize the Witness API client.

        :param base_url: Base URL of the Witness API.
        :param token: Optional Bearer token for authenticated endpoints.
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle the HTTP response, raising exceptions for error codes.

        :param response: The HTTP response object.
        :return: The JSON content of the response.
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            try:
                error_data = response.json()
                message = error_data.get('message', 'An error occurred.')
                code = error_data.get('code')
                issues = error_data.get('issues', [])
                raise WitnessError(message=message, code=code, issues=issues) from http_err
            except ValueError:
                # Response content is not JSON
                raise WitnessError(message=f"HTTP Error occurred: {http_err}") from http_err
        except requests.exceptions.RequestException as req_err:
            # Handle other request exceptions
            raise WitnessError(message=f"Request Error occurred: {req_err}") from req_err

        try:
            return response.json()
        except ValueError:
            # Response content is not JSON
            raise WitnessError(message='Invalid JSON response received.')

    def health(self) -> Dict[str, Any]:
        """
        Health check endpoint.

        :return: Health status of the API.
        """
        response = self.session.get(f'{self.base_url}/_health')
        return self._handle_response(response)

    def get_latest_checkpoint(self, chainId: int = 8453) -> Dict[str, Any]:
        """
        Returns the latest on-chain checkpoint.

        :param chainId: Chain ID of the checkpoint (default: 8453).
        :return: Latest checkpoint data.
        """
        params = {'chainId': chainId}
        response = self.session.get(f'{self.base_url}/getLatestCheckpoint', params=params)
        return self._handle_response(response)

    def get_latest_checkpoint_for_all_chains(self) -> Dict[str, Any]:
        """
        Returns the latest on-chain checkpoint for all chains.

        :return: Latest checkpoints for all chains.
        """
        response = self.session.get(f'{self.base_url}/getLatestCheckpointForAllChains')
        return self._handle_response(response)

    def get_earliest_checkpoint_covering_leaf_index(self, leafIndex: str, chainId: int = 8453) -> Dict[str, Any]:
        """
        Get earliest checkpoint covering a specific leaf index.

        :param leafIndex: Leaf index to query.
        :param chainId: Chain ID of the checkpoint (default: 8453).
        :return: Checkpoint data.
        """
        params = {'leafIndex': leafIndex, 'chainId': chainId}
        response = self.session.get(f'{self.base_url}/getEarliestCheckpointCoveringLeafIndex', params=params)
        return self._handle_response(response)

    def get_checkpoint_by_transaction_hash(self, txHash: str) -> Dict[str, Any]:
        """
        Get a checkpoint by its transaction hash.

        :param txHash: Transaction hash of the checkpoint.
        :return: Checkpoint data.
        """
        params = {'txHash': txHash}
        response = self.session.get(f'{self.base_url}/getCheckpointByTransactionHash', params=params)
        return self._handle_response(response)

    def get_checkpoint_by_timestamp(self, timestamp: str, chainId: int = 8453) -> Dict[str, Any]:
        """
        Get the first checkpoint at or after a unix timestamp.

        :param timestamp: Timestamp to query (in unix epoch seconds).
        :param chainId: Chain ID of the checkpoint (default: 8453).
        :return: Checkpoint data.
        """
        params = {'timestamp': timestamp, 'chainId': chainId}
        response = self.session.get(f'{self.base_url}/getCheckpointByTimestamp', params=params)
        return self._handle_response(response)

    def get_leaf_index_by_hash(self, leafHash: str) -> Dict[str, Any]:
        """
        Get leaf index by its hash.

        :param leafHash: Leaf hash.
        :return: Leaf index.
        """
        params = {'leafHash': leafHash}
        response = self.session.get(f'{self.base_url}/getLeafIndexByHash', params=params)
        return self._handle_response(response)

    def get_timestamp_by_leaf_hash(self, leafHash: str, chainId: int = 8453) -> Dict[str, Any]:
        """
        Get timestamp by leaf hash.

        :param leafHash: Leaf hash.
        :param chainId: Chain ID (default: 8453).
        :return: Timestamp data.
        """
        params = {'leafHash': leafHash, 'chainId': chainId}
        response = self.session.get(f'{self.base_url}/getTimestampByLeafHash', params=params)
        return self._handle_response(response)

    def get_node_hash_by_id(self, level: str, index: str) -> Dict[str, Any]:
        """
        Get node hash by level and index.

        :param level: Node level.
        :param index: Node index.
        :return: Node hash.
        """
        params = {'level': level, 'index': index}
        response = self.session.get(f'{self.base_url}/getNodeHashById', params=params)
        return self._handle_response(response)

    def get_proof_for_leaf_hash(self, leafHash: str, targetTreeSize: Optional[str] = None, chainId: int = 8453) -> Dict[str, Any]:
        """
        Returns the proof for the given leafHash.

        :param leafHash: Leaf hash.
        :param targetTreeSize: Optional target tree size.
        :param chainId: Chain ID (default: 8453).
        :return: Proof data.
        """
        params = {'leafHash': leafHash, 'chainId': chainId}
        if targetTreeSize:
            params['targetTreeSize'] = targetTreeSize
        response = self.session.get(f'{self.base_url}/getProofForLeafHash', params=params)
        return self._handle_response(response)

    def post_proof(self, proof_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a proof.

        :param proof_data: Proof data including leftHashes, rightHashes, targetRootHash, leafHash, and leafIndex.
        :return: Verification result.
        """
        response = self.session.post(f'{self.base_url}/postProof', json=proof_data)
        return self._handle_response(response)

    def get_tree_state(self) -> Dict[str, Any]:
        """
        Get the current state of the tree.

        :return: Tree state data.
        """
        response = self.session.get(f'{self.base_url}/getTreeState')
        return self._handle_response(response)

    def post_leaf_hash(self, leafHash: str) -> Dict[str, Any]:
        """
        Insert a new leaf hash into the tree.

        :param leafHash: The leaf hash to insert.
        :return: Inserted leaf hash and index.
        """
        data = {'leafHash': leafHash}
        response = self.session.post(f'{self.base_url}/postLeafHash', json=data)
        return self._handle_response(response)
    
