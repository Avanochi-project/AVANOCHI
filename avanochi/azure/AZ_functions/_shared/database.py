# shared/database.py

import logging
import uuid
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from _shared.credential_manager import CredentialManager

# Configure logging globally
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class DatabaseError(Exception):
    # Custom exception wrapper for all CosmosDB-related errors.
    pass

class CosmosDBService:
    
    # Service class responsible for handling all interactions with Azure Cosmos DB.
    # Credentials must always come from CredentialManager to ensure single responsibility.

    def __init__(self, credential_manager: CredentialManager):
        self._credential_manager = credential_manager
        self._client = None
        self._database = None
        self._container = None

    def _ensure_connection(self):
        # Initialize Cosmos client, database, and container lazily if not already created.
        if self._client is None:
            creds = self._credential_manager.get_cosmos_credentials()
            url = creds["uri"]
            key = creds["primary_key"]
            database_name = creds["database_name"]
            container_name = creds["container_name"]

            # Create the Cosmos client
            self._client = CosmosClient(url, key)

            # Ensure the database exists
            self._database = self._client.create_database_if_not_exists(id=database_name)

            # Ensure the container exists
            self._container = self._database.create_container_if_not_exists(
                id=container_name,
                partition_key=PartitionKey(path="/id"),
                offer_throughput=400
            )

    @property
    def container(self):
        # Expose the container proxy for direct operations.
        return self._container

    # ==============================
    #    Generic CRUD operations
    # ==============================

    def create_item(self, item: dict) -> dict:

        self._ensure_connection()
        try:
            # Ensure unique ID
            if "id" not in item:
                item["id"] = str(uuid.uuid4())

            created = self._container.create_item(body=item)
            logging.info(f"Item created with id={created['id']}")
            return created
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Failed to create item: {e.message}")
            raise DatabaseError(f"Failed to create item: {e.message}") from e

    def read_item(self, item_id: str, partition_key: str) -> dict:

        # Read a single item from the container.

        self._ensure_connection()
        try:
            return self._container.read_item(item=item_id, partition_key=partition_key)
        except exceptions.CosmosResourceNotFoundError:
            raise DatabaseError(f"Item with id '{item_id}' not found.")
        except exceptions.CosmosHttpResponseError as e:
            raise DatabaseError(f"Failed to read item '{item_id}': {e.message}") from e

    def upsert_item(self, item: dict) -> dict:

        self._ensure_connection()

        try:
            if "id" not in item:
                item["id"] = str(uuid.uuid4())

            if "user_id" not in item:
                raise DatabaseError("Missing required field: 'user_id'")

            upserted = self._container.upsert_item(body=item)
            logging.info(f"Item upserted with id={upserted['id']}")
            return upserted
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Failed to upsert item: {e.message}")
            raise DatabaseError(f"Failed to upsert item: {e.message}") from e


    def delete_item(self, item_id: str, partition_key: str) -> None:

        # Delete an item by id.
        
        self._ensure_connection()
        try:
            logging.info(f"Attempting to delete item with id={item_id}")
            self._container.delete_item(item=item_id, partition_key=partition_key)
        except exceptions.CosmosResourceNotFoundError:
            raise DatabaseError(f"Item with id '{item_id}' not found, cannot delete.")
        except exceptions.CosmosHttpResponseError as e:
            raise DatabaseError(f"Failed to delete item '{item_id}': {e.message}") from e

    def send_query(self, query: str, parameters: list = None) -> list[dict]:
        
        # Execute a query against the container.

        self._ensure_connection()
        if parameters is None:
            parameters = []
        try:
            logging.debug(f"Executing query: {query} | Parameters: {parameters or 'None'}")
            results = self._container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            )
            return [item for item in results]
        except exceptions.CosmosHttpResponseError as e:
            raise DatabaseError(f"Query failed: {e.message}") from e