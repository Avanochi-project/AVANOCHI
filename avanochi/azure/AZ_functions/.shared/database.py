# shared/database.py
from azure.cosmos import CosmosClient, PartitionKey
from shared.credential_manager import CredentialManager

class CosmosDBService:
    
    # Service class responsible for handling all interactions with Azure Cosmos DB.
    # Credentials must always come from CredentialManager to ensure single responsibility.

    def __init__(self, credential_manager: CredentialManager):
        # Initialize the Cosmos DB client and ensure the database and container exist.
        
        creds = credential_manager.get_cosmos_db_credentials()
        self._url = creds["uri"]
        self._key = creds["primary_key"]
        self._database_name = creds["database_name"]
        self._container_name = creds["container_name"]

        # Create the Cosmos client
        self._client = CosmosClient(self._url, self._key)

        # Ensure the database exists
        self._database = self._client.create_database_if_not_exists(id=self._database_name)

        # Ensure the container exists
        self._container = self._database.create_container_if_not_exists(
            id=self._container_name,
            partition_key=PartitionKey(path="/id"),  # Default partition key
            offer_throughput=400
        )

    @property
    def container(self):
        """Expose the container proxy for direct operations."""
        return self._container
